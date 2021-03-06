from rpython.jit.codewriter.policy import JitPolicy

from topaz.main import create_entry_point, get_topaz_config_options


def target(driver, args):
    driver.exe_name = "bin/topaz"
    driver.config.set(**get_topaz_config_options())
    return create_entry_point(driver.config), None


def jitpolicy(driver):
    return JitPolicy()


def handle_config(config, translateconfig):
    config.translation.suggest(check_str_without_nul=True)
