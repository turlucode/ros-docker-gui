import importlib.resources
from string import Template

from loguru import logger

from turludock.config_sanity import is_cuda_cudnn_version_combination_supported, is_cuda_version_supported
from turludock.yaml_load import load_cuda_config, load_cudnn_config


def generate_cuda_base(cuda_version: str, ubuntu_version: str) -> str:
    """Populate the cuda_base.txt template file and return the generated string

    The CUDA and Ubuntu version are used to select the correct CUDA configuration.

    Args:
        cuda_version (str): CUDA version
        ubuntu_version (str): Ubuntu version

    Returns:
        str: dockerfile contents
    """
    logger.debug(f"Generate 'nvidia-cuda-base-{cuda_version}-{ubuntu_version}'")

    # Check if provided version is supported
    if not is_cuda_version_supported(cuda_version, ubuntu_version):
        raise ValueError("CUDA version not supported. Check your configuration.")

    cuda_config = load_cuda_config()[cuda_version][ubuntu_version]

    # Map the template variables
    mapping = {
        "cuda_version": cuda_version,
        "ubuntu_version": ubuntu_version,
        "nvidia_require_cuda": cuda_config["nvidia_require_cuda"],
        "cuda_cudart_version": cuda_config["cudart"],
        "cuda_compat_version": cuda_config["compat"],
    }

    # Populate the templated file
    package = "turludock.assets.dockerfile_templates.nvidia"
    with importlib.resources.open_text(package, "cuda_base.txt") as f:
        src = Template(f.read())
        str_output = src.substitute(mapping)
    str_output += "\n\n"
    return str_output


def generate_cuda_devel(cuda_version: str, ubuntu_version: str) -> str:
    """Populate the cuda_devel.txt template file and return the generated string

    The CUDA and Ubuntu version are used to select the correct CUDA configuration.

    Args:
        cuda_version (str): CUDA version
        ubuntu_version (str): Ubuntu version

    Returns:
        str: dockerfile contents
    """
    logger.debug(f"Generate 'nvidia-cuda-devel-{cuda_version}-{ubuntu_version}'")

    # Check if provided version is supported
    if not is_cuda_version_supported(cuda_version, ubuntu_version):
        raise ValueError("CUDA version not supported. Check your configuration.")

    cuda_config = load_cuda_config()[cuda_version][ubuntu_version]

    # Map the template variables
    mapping = {
        "cuda_cudart_version": cuda_config["cudart"],
        "cuda_lib_version": cuda_config["cuda_lib"],
        "cuda_nvml_version": cuda_config["nvml"],
        "cuda_nvprof_version": cuda_config["nvprof"],
        "cuda_libnpp_version": cuda_config["libnpp"],
        "cuda_libcusparse_version": cuda_config["libcusparse"],
        "cuda_libcublas_version": cuda_config["libcublas"],
        "cuda_libnccl_version": cuda_config["libnccl"],
        "cuda_nsight_compute_version": cuda_config["nsight_compute"],
    }

    # Populate the templated file
    package = "turludock.assets.dockerfile_templates.nvidia"
    with importlib.resources.open_text(package, "cuda_devel.txt") as f:
        src = Template(f.read())
        str_output = src.substitute(mapping)
    str_output += "\n\n"
    return str_output


def generate_cuda_runtime(cuda_version: str, ubuntu_version: str) -> str:
    """Populate the cuda_runtime.txt template file and return the generated string

    The CUDA and Ubuntu version are used to select the correct CUDA configuration.

    Args:
        cuda_version (str): CUDA version
        ubuntu_version (str): Ubuntu version

    Returns:
        str: dockerfile contents
    """
    logger.debug(f"Generate 'nvidia-cuda-runtime-{cuda_version}-{ubuntu_version}'")

    # Check if provided version is supported
    if not is_cuda_version_supported(cuda_version, ubuntu_version):
        raise ValueError("CUDA version not supported. Check your configuration.")

    cuda_config = load_cuda_config()[cuda_version][ubuntu_version]

    # Map the template variables
    mapping = {
        "cuda_lib_version": cuda_config["cuda_lib"],
        "cuda_libnpp_version": cuda_config["libnpp"],
        "cuda_nvtx_version": cuda_config["nvtx"],
        "cuda_libcusparse_version": cuda_config["libcusparse"],
        "cuda_libcublas_version": cuda_config["libcublas"],
        "cuda_libnccl_version": cuda_config["libnccl"],
    }

    # Populate the templated file
    package = "turludock.assets.dockerfile_templates.nvidia"
    with importlib.resources.open_text(package, "cuda_runtime.txt") as f:
        src = Template(f.read())
        str_output = src.substitute(mapping)
    str_output += "\n\n"
    return str_output


def generate_cudnn_devel(cuda_version: str, cudnn_version: str, ubuntu_version: str) -> str:
    """Populate the cudnn_devel.txt template file and return the generated string

    The CUDA, cuDNN and Ubuntu version are used to select the correct cuDNN configuration.

    Args:
        cuda_version (str): CUDA version
        cudnn_version (str): cuDNN version
        ubuntu_version (str): Ubuntu version

    Returns:
        str: dockerfile contents
    """
    logger.debug(f"Generate 'nvidia-cudnn-devel-{cudnn_version}-{ubuntu_version}'")

    # Check if provided version is supported
    if not is_cuda_cudnn_version_combination_supported(cuda_version, cudnn_version, ubuntu_version):
        raise ValueError("cuDNN version not supported. Check your configuration.")

    cudnn_config = load_cudnn_config()[cudnn_version][ubuntu_version]

    # Map the template variables
    mapping = {
        "libcudnn_package": cudnn_config["libcudnn_package"],
        "libcudnn_dev_package": cudnn_config["libcudnn_dev_package"],
        "libcudnn_version": cudnn_config["libcudnn_version"],
        "libcudnn_revision": cudnn_config["libcudnn_revision"],
    }

    # Populate the templated file
    package = "turludock.assets.dockerfile_templates.nvidia"
    with importlib.resources.open_text(package, "cudnn_devel.txt") as f:
        src = Template(f.read())
        str_output = src.substitute(mapping)
    str_output += "\n\n"
    return str_output


def generate_cudnn_runtime(cuda_version: str, cudnn_version: str, ubuntu_version: str) -> str:
    """Populate the cudnn_runtime.txt template file and return the generated string

    The CUDA, cuDNN and Ubuntu version are used to select the correct cuDNN configuration.

    Args:
        cuda_version (str): CUDA version
        cudnn_version (str): cuDNN version
        ubuntu_version (str): Ubuntu version

    Returns:
        str: dockerfile contents
    """
    logger.debug(f"Generate 'nvidia-cudnn-runtime-{cudnn_version}-{ubuntu_version}'")

    # Check if provided version is supported
    if not is_cuda_cudnn_version_combination_supported(cuda_version, cudnn_version, ubuntu_version):
        raise ValueError("cuDNN version not supported. Check your configuration.")

    cudnn_config = load_cudnn_config()[cudnn_version][ubuntu_version]

    # Map the template variables
    mapping = {
        "libcudnn_package": cudnn_config["libcudnn_package"],
        "libcudnn_version": cudnn_config["libcudnn_version"],
        "libcudnn_revision": cudnn_config["libcudnn_revision"],
    }

    # Populate the templated file
    package = "turludock.assets.dockerfile_templates.nvidia"
    with importlib.resources.open_text(package, "cudnn_runtime.txt") as f:
        src = Template(f.read())
        str_output = src.substitute(mapping)
    str_output += "\n\n"
    return str_output
