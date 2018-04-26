#!/usr/bin/env python
# coding=utf-8
"""
A example usage of the AutoCompleter

Copyright 2018 Eric Lin <anselor@gmail.com>
Released under MIT license, see LICENSE file
"""
import argparse
import itertools
from typing import List

import cmd2
from cmd2 import with_argparser, with_category, argparse_completer

actors = ['Mark Hamill', 'Harrison Ford', 'Carrie Fisher', 'Alec Guinness', 'Peter Mayhew',
          'Anthony Daniels', 'Adam Driver', 'Daisy Ridley', 'John Boyega', 'Oscar Isaac',
          'Lupita Nyong\'o', 'Andy Serkis', 'Liam Neeson', 'Ewan McGregor', 'Natalie Portman',
          'Jake Lloyd', 'Hayden Christensen', 'Christopher Lee']

def query_actors() -> List[str]:
    """Simulating a function that queries and returns a completion values"""
    return actors


class TabCompleteExample(cmd2.Cmd):
    """ Example cmd2 application where we a base command which has a couple subcommands."""

    CAT_AUTOCOMPLETE = 'AutoComplete Examples'

    def __init__(self):
        super().__init__()

    # For mocking a data source for the example commands
    ratings_types = ['G', 'PG', 'PG-13', 'R', 'NC-17']
    show_ratings = ['TV-Y', 'TV-Y7', 'TV-G', 'TV-PG', 'TV-14', 'TV-MA']
    static_list_directors = ['J. J. Abrams', 'Irvin Kershner', 'George Lucas', 'Richard Marquand',
                             'Rian Johnson', 'Gareth Edwards']
    USER_MOVIE_LIBRARY = ['ROGUE1', 'SW_EP04', 'SW_EP05']
    MOVIE_DATABASE_IDS = ['SW_EP01', 'SW_EP02', 'SW_EP03', 'ROGUE1', 'SW_EP04',
                          'SW_EP05', 'SW_EP06', 'SW_EP07', 'SW_EP08', 'SW_EP09']
    MOVIE_DATABASE = {'SW_EP04': {'title': 'Star Wars: Episode IV - A New Hope',
                                  'rating': 'PG',
                                  'director': ['George Lucas'],
                                  'actor': ['Mark Hamill', 'Harrison Ford', 'Carrie Fisher',
                                            'Alec Guinness', 'Peter Mayhew', 'Anthony Daniels']
                                  },
                      'SW_EP05': {'title': 'Star Wars: Episode V - The Empire Strikes Back',
                                  'rating': 'PG',
                                  'director': ['Irvin Kershner'],
                                  'actor': ['Mark Hamill', 'Harrison Ford', 'Carrie Fisher',
                                            'Alec Guinness', 'Peter Mayhew', 'Anthony Daniels']
                                  },
                      'SW_EP06': {'title': 'Star Wars: Episode IV - A New Hope',
                                  'rating': 'PG',
                                  'director': ['Richard Marquand'],
                                  'actor': ['Mark Hamill', 'Harrison Ford', 'Carrie Fisher',
                                            'Alec Guinness', 'Peter Mayhew', 'Anthony Daniels']
                                  },
                      'SW_EP01': {'title': 'Star Wars: Episode I - The Phantom Menace',
                                  'rating': 'PG',
                                  'director': ['George Lucas'],
                                  'actor': ['Liam Neeson', 'Ewan McGregor', 'Natalie Portman', 'Jake Lloyd']
                                  },
                      'SW_EP02': {'title': 'Star Wars: Episode II - Attack of the Clones',
                                  'rating': 'PG',
                                  'director': ['George Lucas'],
                                  'actor': ['Liam Neeson', 'Ewan McGregor', 'Natalie Portman',
                                            'Hayden Christensen', 'Christopher Lee']
                                  },
                      'SW_EP03': {'title': 'Star Wars: Episode III - Revenge of the Sith',
                                  'rating': 'PG-13',
                                  'director': ['George Lucas'],
                                  'actor': ['Liam Neeson', 'Ewan McGregor', 'Natalie Portman',
                                            'Hayden Christensen']
                                  },

                      }
    USER_SHOW_LIBRARY = {'SW_REB': ['S01E01', 'S02E02']}
    SHOW_DATABASE_IDS = ['SW_CW', 'SW_TCW', 'SW_REB']
    SHOW_DATABASE = {'SW_CW':   {'title': 'Star Wars: Clone Wars',
                                 'rating': 'TV-Y7',
                                 'seasons': {1: ['S01E01', 'S01E02', 'S01E03'],
                                             2: ['S02E01', 'S02E02', 'S02E03']}
                                 },
                     'SW_TCW':  {'title': 'Star Wars: The Clone Wars',
                                 'rating': 'TV-PG',
                                 'seasons': {1: ['S01E01', 'S01E02', 'S01E03'],
                                             2: ['S02E01', 'S02E02', 'S02E03']}
                                 },
                     'SW_REB':  {'title': 'Star Wars: Rebels',
                                 'rating': 'TV-Y7',
                                 'seasons': {1: ['S01E01', 'S01E02', 'S01E03'],
                                             2: ['S02E01', 'S02E02', 'S02E03']}
                                 },
                     }

    def instance_query_actors(self) -> List[str]:
        """Simulating a function that queries and returns a completion values"""
        return actors

    # This demonstrates a number of customizations of the AutoCompleter version of ArgumentParser
    #  - The help output will separately group required vs optional flags
    #  - The help output for arguments with multiple flags or with append=True is more concise
    #  - ACArgumentParser adds the ability to specify ranges of argument counts in 'nargs'

    suggest_parser = argparse_completer.ACArgumentParser()

    suggest_parser.add_argument('-t', '--type', choices=['movie', 'show'], required=True)
    suggest_parser.add_argument('-d', '--duration', nargs=(1, 2), action='append',
                                help='Duration constraint in minutes.\n'
                                     '\tsingle value - maximum duration\n'
                                     '\t[a, b] - duration range')

    @with_category(CAT_AUTOCOMPLETE)
    @with_argparser(suggest_parser)
    def do_suggest(self, args) -> None:
        """Suggest command demonstrates argparse customizations

        See hybrid_suggest and orig_suggest to compare the help output.


        """
        if not args.type:
            self.do_help('suggest')

    # If you prefer the original argparse help output but would like narg ranges, it's possible
    # to enable narg ranges without the help changes using this method

    suggest_parser_hybrid = argparse.ArgumentParser()
    # This registers the custom narg range handling
    argparse_completer.register_custom_actions(suggest_parser_hybrid)

    suggest_parser_hybrid.add_argument('-t', '--type', choices=['movie', 'show'], required=True)
    suggest_parser_hybrid.add_argument('-d', '--duration', nargs=(1, 2), action='append',
                                       help='Duration constraint in minutes.\n'
                                            '\tsingle value - maximum duration\n'
                                            '\t[a, b] - duration range')

    @with_category(CAT_AUTOCOMPLETE)
    @with_argparser(suggest_parser_hybrid)
    def do_hybrid_suggest(self, args):
        if not args.type:
            self.do_help('orig_suggest')

    # This variant demonstrates the AutoCompleter working with the orginial argparse.
    # Base argparse is unable to specify narg ranges. Autocompleter will keep expecting additional arguments
    # for the -d/--duration flag until you specify a new flaw or end the list it with '--'

    suggest_parser_orig = argparse.ArgumentParser()

    suggest_parser_orig.add_argument('-t', '--type', choices=['movie', 'show'], required=True)
    suggest_parser_orig.add_argument('-d', '--duration', nargs='+', action='append',
                                     help='Duration constraint in minutes.\n'
                                          '\tsingle value - maximum duration\n'
                                          '\t[a, b] - duration range')

    @with_argparser(suggest_parser_orig)
    @with_category(CAT_AUTOCOMPLETE)
    def do_orig_suggest(self, args) -> None:
        if not args.type:
            self.do_help('orig_suggest')

    ###################################################################################
    # The media command demonstrates a completer with multiple layers of subcommands
    #   - This example demonstrates how to tag a completion attribute on each action, enabling argument
    #       completion without implementing a complete_COMMAND function

    def _do_vid_media_movies(self, args) -> None:
        if not args.command:
            self.do_help('media movies')
        elif args.command == 'list':
            for movie_id in TabCompleteExample.MOVIE_DATABASE:
                movie = TabCompleteExample.MOVIE_DATABASE[movie_id]
                print('{}\n-----------------------------\n{}   ID: {}\nDirector: {}\nCast:\n    {}\n\n'
                      .format(movie['title'], movie['rating'], movie_id,
                              ', '.join(movie['director']),
                              '\n    '.join(movie['actor'])))

    def _do_vid_media_shows(self, args) -> None:
        if not args.command:
            self.do_help('media shows')

        elif args.command == 'list':
            for show_id in TabCompleteExample.SHOW_DATABASE:
                show = TabCompleteExample.SHOW_DATABASE[show_id]
                print('{}\n-----------------------------\n{}   ID: {}'
                      .format(show['title'], show['rating'], show_id))
                for season in show['seasons']:
                    ep_list = show['seasons'][season]
                    print('  Season {}:\n    {}'
                          .format(season,
                                  '\n    '.join(ep_list)))
                print()

    video_parser = argparse_completer.ACArgumentParser(prog='media')

    video_types_subparsers = video_parser.add_subparsers(title='Media Types', dest='type')

    vid_movies_parser = video_types_subparsers.add_parser('movies')
    vid_movies_parser.set_defaults(func=_do_vid_media_movies)

    vid_movies_commands_subparsers = vid_movies_parser.add_subparsers(title='Commands', dest='command')

    vid_movies_list_parser = vid_movies_commands_subparsers.add_parser('list')

    vid_movies_list_parser.add_argument('-t', '--title', help='Title Filter')
    vid_movies_list_parser.add_argument('-r', '--rating', help='Rating Filter', nargs='+',
                                        choices=ratings_types)
    # save a reference to the action object
    director_action = vid_movies_list_parser.add_argument('-d', '--director', help='Director Filter')
    actor_action = vid_movies_list_parser.add_argument('-a', '--actor', help='Actor Filter', action='append')

    # tag the action objects with completion providers. This can be a collection or a callable
    setattr(director_action, argparse_completer.ACTION_ARG_CHOICES, static_list_directors)
    setattr(actor_action, argparse_completer.ACTION_ARG_CHOICES, query_actors)

    vid_movies_add_parser = vid_movies_commands_subparsers.add_parser('add')
    vid_movies_add_parser.add_argument('title', help='Movie Title')
    vid_movies_add_parser.add_argument('rating', help='Movie Rating', choices=ratings_types)

    # save a reference to the action object
    director_action = vid_movies_add_parser.add_argument('-d', '--director', help='Director', nargs=(1, 2),
                                                         required=True)
    actor_action = vid_movies_add_parser.add_argument('actor', help='Actors', nargs='*')

    # tag the action objects with completion providers. This can be a collection or a callable
    setattr(director_action, argparse_completer.ACTION_ARG_CHOICES, static_list_directors)
    setattr(actor_action, argparse_completer.ACTION_ARG_CHOICES, instance_query_actors)

    vid_movies_delete_parser = vid_movies_commands_subparsers.add_parser('delete')

    vid_shows_parser = video_types_subparsers.add_parser('shows')
    vid_shows_parser.set_defaults(func=_do_vid_media_shows)

    vid_shows_commands_subparsers = vid_shows_parser.add_subparsers(title='Commands', dest='command')

    vid_shows_list_parser = vid_shows_commands_subparsers.add_parser('list')

    @with_category(CAT_AUTOCOMPLETE)
    @with_argparser(video_parser)
    def do_video(self, args):
        """Video management command demonstrates multiple layers of subcommands being handled by AutoCompleter"""
        func = getattr(args, 'func', None)
        if func is not None:
            # Call whatever subcommand function was selected
            func(self, args)
        else:
            # No subcommand was provided, so call help
            self.do_help('video')

    ###################################################################################
    # The media command demonstrates a completer with multiple layers of subcommands
    #   - This example uses a flat completion lookup dictionary

    def _do_media_movies(self, args) -> None:
        if not args.command:
            self.do_help('media movies')
        elif args.command == 'list':
            for movie_id in TabCompleteExample.MOVIE_DATABASE:
                movie = TabCompleteExample.MOVIE_DATABASE[movie_id]
                print('{}\n-----------------------------\n{}   ID: {}\nDirector: {}\nCast:\n    {}\n\n'
                      .format(movie['title'], movie['rating'], movie_id,
                              ', '.join(movie['director']),
                              '\n    '.join(movie['actor'])))

    def _do_media_shows(self, args) -> None:
        if not args.command:
            self.do_help('media shows')

        elif args.command == 'list':
            for show_id in TabCompleteExample.SHOW_DATABASE:
                show = TabCompleteExample.SHOW_DATABASE[show_id]
                print('{}\n-----------------------------\n{}   ID: {}'
                      .format(show['title'], show['rating'], show_id))
                for season in show['seasons']:
                    ep_list = show['seasons'][season]
                    print('  Season {}:\n    {}'
                          .format(season,
                                  '\n    '.join(ep_list)))
                print()

    media_parser = argparse_completer.ACArgumentParser(prog='media')

    media_types_subparsers = media_parser.add_subparsers(title='Media Types', dest='type')

    movies_parser = media_types_subparsers.add_parser('movies')
    movies_parser.set_defaults(func=_do_media_movies)

    movies_commands_subparsers = movies_parser.add_subparsers(title='Commands', dest='command')

    movies_list_parser = movies_commands_subparsers.add_parser('list')

    movies_list_parser.add_argument('-t', '--title', help='Title Filter')
    movies_list_parser.add_argument('-r', '--rating', help='Rating Filter', nargs='+',
                                    choices=ratings_types)
    movies_list_parser.add_argument('-d', '--director', help='Director Filter')
    movies_list_parser.add_argument('-a', '--actor', help='Actor Filter', action='append')

    movies_add_parser = movies_commands_subparsers.add_parser('add')
    movies_add_parser.add_argument('title', help='Movie Title')
    movies_add_parser.add_argument('rating', help='Movie Rating', choices=ratings_types)
    movies_add_parser.add_argument('-d', '--director', help='Director', nargs=(1, 2), required=True)
    movies_add_parser.add_argument('actor', help='Actors', nargs='*')

    movies_delete_parser = movies_commands_subparsers.add_parser('delete')

    shows_parser = media_types_subparsers.add_parser('shows')
    shows_parser.set_defaults(func=_do_media_shows)

    shows_commands_subparsers = shows_parser.add_subparsers(title='Commands', dest='command')

    shows_list_parser = shows_commands_subparsers.add_parser('list')

    @with_category(CAT_AUTOCOMPLETE)
    @with_argparser(media_parser)
    def do_media(self, args):
        """Media management command demonstrates multiple layers of subcommands being handled by AutoCompleter"""
        func = getattr(args, 'func', None)
        if func is not None:
            # Call whatever subcommand function was selected
            func(self, args)
        else:
            # No subcommand was provided, so call help
            self.do_help('media')

    # This completer is implemented using a single dictionary to look up completion lists for all layers of
    # subcommands. For each argument, AutoCompleter will search for completion values from the provided
    # arg_choices dict. This requires careful naming of argparse arguments so that there are no unintentional
    # name collisions.
    def complete_media(self, text, line, begidx, endidx):
        """ Adds tab completion to media"""
        choices = {'actor': query_actors,  # function
                   'director': TabCompleteExample.static_list_directors  # static list
                   }
        completer = argparse_completer.AutoCompleter(TabCompleteExample.media_parser, arg_choices=choices)

        tokens, _ = self.tokens_for_completion(line, begidx, endidx)
        results = completer.complete_command(tokens, text, line, begidx, endidx)

        return results

    ###################################################################################
    # The library command demonstrates a completer with multiple layers of subcommands
    # with different completion results per sub-command
    #   - This demonstrates how to build a tree of completion lookups to pass down
    #
    # Only use this method if you absolutely need to as it dramatically
    # increases the complexity and decreases readability.

    def _do_library_movie(self, args):
        if not args.type or not args.command:
            self.do_help('library movie')

    def _do_library_show(self, args):
        if not args.type:
            self.do_help('library show')

    def _query_movie_database(self):
        return list(set(TabCompleteExample.MOVIE_DATABASE_IDS).difference(set(TabCompleteExample.USER_MOVIE_LIBRARY)))

    def _query_movie_user_library(self):
        return TabCompleteExample.USER_MOVIE_LIBRARY

    def _filter_library(self, text, line, begidx, endidx, full, exclude=()):
        candidates = list(set(full).difference(set(exclude)))
        return [entry for entry in candidates if entry.startswith(text)]

    library_parser = argparse_completer.ACArgumentParser(prog='library')

    library_subcommands = library_parser.add_subparsers(title='Media Types', dest='type')

    library_movie_parser = library_subcommands.add_parser('movie')
    library_movie_parser.set_defaults(func=_do_library_movie)

    library_movie_subcommands = library_movie_parser.add_subparsers(title='Command', dest='command')

    library_movie_add_parser = library_movie_subcommands.add_parser('add')
    library_movie_add_parser.add_argument('movie_id', help='ID of movie to add', action='append')
    library_movie_add_parser.add_argument('-b', '--borrowed', action='store_true')

    library_movie_remove_parser = library_movie_subcommands.add_parser('remove')
    library_movie_remove_parser.add_argument('movie_id', help='ID of movie to remove', action='append')

    library_show_parser = library_subcommands.add_parser('show')
    library_show_parser.set_defaults(func=_do_library_show)

    library_show_subcommands = library_show_parser.add_subparsers(title='Command', dest='command')

    library_show_add_parser = library_show_subcommands.add_parser('add')
    library_show_add_parser.add_argument('show_id', help='Show IDs to add')
    library_show_add_parser.add_argument('episode_id', nargs='*', help='Show IDs to add')

    library_show_rmv_parser = library_show_subcommands.add_parser('remove')

    # Demonstrates a custom completion function that does more with the command line than is
    # allowed by the standard completion functions
    def _filter_episodes(self, text, line, begidx, endidx, show_db, user_lib):
        tokens, _ = self.tokens_for_completion(line, begidx, endidx)
        show_id = tokens[3]
        if show_id:
            if show_id in show_db:
                show = show_db[show_id]
                all_episodes = itertools.chain(*(show['seasons'].values()))

                if show_id in user_lib:
                    user_eps = user_lib[show_id]
                else:
                    user_eps = []

                return self._filter_library(text, line, begidx, endidx, all_episodes, user_eps)
        return []

    @with_category(CAT_AUTOCOMPLETE)
    @with_argparser(library_parser)
    def do_library(self, args):
        """Media management command demonstrates multiple layers of subcommands being handled by AutoCompleter"""
        func = getattr(args, 'func', None)
        if func is not None:
            # Call whatever subcommand function was selected
            func(self, args)
        else:
            # No subcommand was provided, so call help
            self.do_help('library')

    def complete_library(self, text, line, begidx, endidx):

        # this demonstrates the much more complicated scenario of having
        # unique completion parameters per sub-command that use the same
        # argument name. To do this we build a multi-layer nested tree
        # of lookups far AutoCompleter to traverse. This nested tree must
        # match the structure of the argparse parser
        #

        movie_add_choices = {'movie_id': self._query_movie_database}
        movie_remove_choices = {'movie_id': self._query_movie_user_library}

        # This demonstrates the ability to mix custom completion functions with argparse completion.
        # By specifying a tuple for a completer, AutoCompleter expects a custom completion function
        # with optional index-based as well as keyword based arguments. This is an alternative to using
        # a partial function.

        show_add_choices = {'show_id': (self._filter_library,  # This is a custom completion function
                                        # This tuple represents index-based args to append to the function call
                                        (list(TabCompleteExample.SHOW_DATABASE.keys()),)
                                        ),
                            'episode_id': (self._filter_episodes,  # this is a custom completion function
                                           # this list represents index-based args to append to the function call
                                           [TabCompleteExample.SHOW_DATABASE],
                                           # this dict contains keyword-based args to append to the function call
                                           {'user_lib': TabCompleteExample.USER_SHOW_LIBRARY})}
        show_remove_choices = {}

        # The library movie sub-parser group 'command' has 2 sub-parsers:
        #   'add' and 'remove'
        library_movie_command_params = \
            {'add': (movie_add_choices, None),
             'remove': (movie_remove_choices, None)}

        library_show_command_params = \
            {'add': (show_add_choices, None),
             'remove': (show_remove_choices, None)}

        # The 'library movie' command has a sub-parser group called 'command'
        library_movie_subcommand_groups = {'command': library_movie_command_params}
        library_show_subcommand_groups = {'command': library_show_command_params}

        # Mapping of a specific sub-parser of the 'type' group to a tuple. Each
        #    tuple has 2 values corresponding what's passed to the constructor
        #    parameters (arg_choices,subcmd_args_lookup) of the nested
        #    instance of AutoCompleter
        library_type_params = {'movie': (None, library_movie_subcommand_groups),
                               'show': (None, library_show_subcommand_groups)}

        # maps the a subcommand group to a dictionary mapping a specific
        # sub-command to a tuple of (arg_choices, subcmd_args_lookup)
        #
        # In this example, 'library_parser' has a sub-parser group called 'type'
        #   under the type sub-parser group, there are 2 sub-parsers: 'movie', 'show'
        library_subcommand_groups = {'type': library_type_params}

        completer = argparse_completer.AutoCompleter(TabCompleteExample.library_parser,
                                                     subcmd_args_lookup=library_subcommand_groups)

        tokens, _ = self.tokens_for_completion(line, begidx, endidx)
        results = completer.complete_command(tokens, text, line, begidx, endidx)

        return results


if __name__ == '__main__':
    app = TabCompleteExample()
    app.cmdloop()