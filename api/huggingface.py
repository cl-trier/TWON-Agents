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

class Prompt(pydantic.BaseModel):
    system: str = ""
    user: str

class HuggingfaceInferenceConfig(pydantic.BaseModel):
    input_max_length: int = 200

    temperature: float = 0.7
    output_max_length: int = 64
    repetition_penalty: float = 1.2


class Huggingface(Interface):
    auth_token: str

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

    def inference(self, prompts: typing.List[Prompt], inference_config: HuggingfaceInferenceConfig) -> typing.List[str]:
        encodings: transformers.BatchEncoding = self._tokenize(prompts, inference_config)

        return self._tokenizer.batch_decode(
            self._generate(encodings, inference_config)[:, encodings.input_ids.shape[1] :],
            skip_special_tokens=True,
        )

    def _tokenize(self, prompts: typing.List[Prompt], inference_config: HuggingfaceInferenceConfig) -> transformers.BatchEncoding:
        return self._tokenizer(
            [
                self._tokenizer.apply_chat_template(
                    [
                        {"role": "system", "content": prompt.system},
                        {"role": "user", "content": prompt.user},
                    ],
                    tokenize=False,
                )
                for prompt in prompts
            ],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=inference_config.input_max_length,
        ).to("cuda")

    @torch.no_grad()
    def _generate(
        self,
        batch: transformers.BatchEncoding,
        inference_config: HuggingfaceInferenceConfig
    ) -> typing.Any:
        return self._model.generate(
            **batch,
            temperature=inference_config.temperature,
            max_new_tokens=inference_config.output_max_length,
            do_sample=True,
            repetition_penalty=inference_config.repetition_penalty,
        )
    



class InferenceFinetunedRequest(pydantic.BaseModel):
    model: typing.Literal["left", "right"]

    prompts: typing.List[Prompt] 

    config: HuggingfaceInferenceConfig = HuggingfaceInferenceConfig()