Import("env")
from pathlib import Path
import sys
from os.path import join
import subprocess

def post_program_action(source, target, env):
    print("mohan")
    #print(dir(env))
    print(env.subst("$PROGNAME"))
    tool = env.subst(env["MKFSTOOL"])
    print(tool)
    flash_size = env.BoardConfig().get("upload.flash_size")
    flash_mode = env["__get_board_flash_mode"](env)
    flash_freq = env["__get_board_f_flash"](env)
    chip = env.get("BOARD_MCU")
    build_dir = env.subst("$BUILD_DIR")
    new_filename = Path(build_dir) / env.subst("${PROGNAME}.factory.bin")
    bootloader = Path(build_dir) / "bootloader.bin"
    partitions = Path(build_dir) / "partitions.bin"
    firmware = Path(build_dir) / env.subst("${PROGNAME}.bin")
    print(flash_size)
    print(flash_mode)
    print(flash_freq)
    print(bootloader)
    print(partitions)
    print(firmware)

    print(chip)
    cmd = [
        "--chip",
        chip,
        "merge_bin",
        "-o",
        str(new_filename),
        "--flash_mode",
        flash_mode,
        "--flash_freq",
        flash_freq,
        "--flash_size",
        flash_size
    ]

    littlefs_data = "data"
    littlefs = join(env.subst("$BUILD_DIR"),"littlefs.bin")
    fs_size = "1408000"
    littlefscmd = (tool,"-c",littlefs_data,"-s",fs_size,littlefs)
    #cmd = (tool, "-h")
    subprocess.call(littlefscmd, shell=False)
    littlefscmd = (tool, "-l", littlefs)
    subprocess.call(littlefscmd, shell=False)

    cmd += ["0x1000", str(bootloader)]
    cmd += ["0x8000", str(partitions)]
    cmd += ["0x10000", str(firmware)]
    cmd += ["0x290000", str(littlefs)]
    print(cmd)
    platform = env.PioPlatform()
    sys.path.append(join(platform.get_package_dir("tool-esptoolpy")))
    import esptool
    esptool.main(cmd)


env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", post_program_action)