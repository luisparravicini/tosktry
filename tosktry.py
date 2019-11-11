#!/usr/bin/env python3

import argparse
import tosktry

parser = argparse.ArgumentParser()
parser.add_argument('-b', dest='bot', action='store_true',
                    help='enables the bot')

args = parser.parse_args()
game = tosktry.Game()
game.enable_bot(args.bot)
game.run()
