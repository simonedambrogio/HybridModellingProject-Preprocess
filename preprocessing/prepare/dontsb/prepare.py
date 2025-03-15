from .prepare_struct import _prepare_struct
from .prepare_bold4d import _prepare_bold4d
from .prepare_fmap import _prepare_fmap
from .prepare_boldwb import _prepare_boldwb


def prepare(config, subject: int, session: int, input_dir: str, output_dir: str, submit: bool, submit_to: str = "slurm"):
    _prepare_struct(config, subject, session, input_dir, output_dir, submit, submit_to)
    _prepare_bold4d(config, subject, session, input_dir, output_dir, submit, submit_to)
    _prepare_fmap(config, subject, session, input_dir, output_dir, submit, submit_to)
    _prepare_boldwb(config, subject, session, input_dir, output_dir, submit, submit_to)
