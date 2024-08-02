import typing

import huggingface_hub
import peft
import pydantic
import torch
import transformers

import abc

import pydantic


class Interface(abc.ABC, pydantic.BaseModel):
    llm_slug: str

    @abc.abstractmethod
    def inference(self, system: str, prompt: str, **kwargs) -> str:
        raise NotImplementedError


class HuggingfaceInferenceConfig(pydantic.BaseModel):
    input_max_length: int = 200

    temperature: float = 0.7
    output_max_length: int = 64
    repetition_penalty: float = 1.2


class Huggingface(Interface):
    auth_token: str

    inference_config: HuggingfaceInferenceConfig = HuggingfaceInferenceConfig()

    _tokenizer: transformers.AutoTokenizer
    _model: peft.PeftModel

    def model_post_init(self, _: typing.Any):
        huggingface_hub.login(token=self.auth_token)

        config = peft.PeftConfig.from_pretrained(self.llm_slug)

        self._tokenizer = transformers.AutoTokenizer.from_pretrained(
            config.base_model_name_or_path
        )

        self._model = peft.PeftModel.from_pretrained(
            transformers.AutoModelForCausalLM.from_pretrained(
                config.base_model_name_or_path,
                quantization_config=transformers.BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.float16,
                ),
                device_map="auto",
                attn_implementation="sdpa",
            ),
            self.llm_slug,
        )

        self._tokenizer.pad_token = self._tokenizer.eos_token

    def inference(self, system: str, prompt: str, **_) -> str:
        encodings: transformers.BatchEncoding = self._tokenize(system, prompt)

        return self._tokenizer.batch_decode(
            self._generate(encodings)[:, encodings.input_ids.shape[1] :],
            skip_special_tokens=True,
        )[0]

    def _tokenize(self, system: str, prompt: str) -> transformers.BatchEncoding:
        return self._tokenizer(
            [
                self._tokenizer.apply_chat_template(
                    [
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                    tokenize=False,
                )
            ],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=self.inference_config.input_max_length,
        ).to("cuda")

    @torch.no_grad()
    def _generate(
        self,
        batch: transformers.BatchEncoding,
    ) -> typing.Any:
        return self._model.generate(
            **batch,
            temperature=self.inference_config.temperature,
            max_new_tokens=self.inference_config.output_max_length,
            do_sample=True,
            repetition_penalty=self.inference_config.repetition_penalty,
        )
    

class InferenceFinetunedRequest(pydantic.BaseModel):
    model: typing.Literal["left", "right"]
    auth_token: str

    prompt: str
    system_prompt: str = ""

    config: HuggingfaceInferenceConfig = HuggingfaceInferenceConfig()

    @pydantic.computed_field  # type: ignore
    @property
    def slug(self):
        return {
            "left": "./models/huggingface/v2_left",
            "right": "./models/huggingface/v2_right"
        }[self.model]