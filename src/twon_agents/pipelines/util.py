import argparse


pipeline_argparser = argparse.ArgumentParser(
    prog="Pipeline Arguments",
    description="Optional Pipeline Arguments",
)

pipeline_argparser.add_argument("--device", nargs="?", const=0, type=int)
pipeline_argparser.add_argument(
    "--train", action=argparse.BooleanOptionalAction, default=True
)
pipeline_argparser.add_argument(
    "--eval", action=argparse.BooleanOptionalAction, default=True
)
