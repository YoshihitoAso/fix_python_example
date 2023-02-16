import sys
import argparse

import quickfix

from application import Application


def main(config_file):
    # Setting
    settings = quickfix.SessionSettings(config_file)
    application = Application()

    store_factory = quickfix.FileStoreFactory(settings)
    log_factory = quickfix.FileLogFactory(settings)
    initiator = quickfix.SocketInitiator(
        application=application,
        storeFactory=store_factory,
        settings=settings,
        logFactory=log_factory
    )

    # Start initiator application
    try:
        initiator.start()
        application.run()
        initiator.stop()
    except (quickfix.ConfigError, quickfix.RuntimeError) as e:
        print(e)
        initiator.stop()
        sys.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='FIX Client')
    parser.add_argument('file_name', type=str, help='Name of configuration file')
    args = parser.parse_args()
    main(args.file_name)
