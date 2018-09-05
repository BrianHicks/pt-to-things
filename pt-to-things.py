#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import argparse
import json
import os
from pprint import pprint
from urllib.parse import quote
import urllib.request as request


class Client:
    def __init__(self, token):
        self.token = token

        if not self.token:
            raise Exception('token cannot be blank/empty')

    def get_json(self, url):
        req = request.Request(url, headers={b'X-TrackerToken': self.token})
        return json.load(request.urlopen(req))

    def story(self, story):
        return Story(self, story)

    def story_tasks(self, project, story):
        req = request.Request(url, headers={'X-TrackerToken': self.token})
        return request.urlopen(req)


class Story:
    def __init__(self, client, id):
        self.client = client
        self.id = id
        self.__body = None
        self.__tasks = None

    @property
    def body(self):
        if self.__body is None:
            self.__body = self.client.get_json(
                'https://www.pivotaltracker.com/services/v5/stories/%s' % self.id
            )

        return self.__body

    @property
    def tasks(self):
        if self.__tasks is None:
            self.__tasks = self.client.get_json(
                'https://www.pivotaltracker.com/services/v5/projects/%s/stories/%s/tasks' % (
                    self.body['project_id'],
                    self.id
                )
            )

        return self.__tasks

    def things_project(self):
        project = {
            'type': 'project',
            'operation': 'create',
            'attributes': {
                'title': self.body['name'],
                'creation-date': self.body['created_at'],
                'notes': self.body.get('description', 'no description set in PT!') + '\n\n' + self.body['url'],
            }
        }

        if self.tasks:
            project['attributes']['items'] = [self.__things_task_body(task) for task in self.tasks]

        return project

    def __things_task_body(self, task):
        return {
            'type': 'to-do',
            'attributes': {
                'title': task['description'],
                'completed': task['complete'],
                'creation-date': task['created_at'],
            }
        }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(__file__)
    parser.add_argument('--token', default=os.environ.get('PT_TOKEN'))
    parser.add_argument('--area')
    parser.add_argument('story')
    args = parser.parse_args()

    client = Client(args.token)
    story = client.story(args.story.strip('#'))

    project = story.things_project()
    if args.area:
        project['area'] = args.area

    print('things:///json?reveal=true&data=%s' % quote(json.dumps([project])))
