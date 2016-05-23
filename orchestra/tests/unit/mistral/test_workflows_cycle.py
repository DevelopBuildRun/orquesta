# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from orchestra import states
from orchestra.tests.unit import base


class CyclicWorkflowConductorTest(base.WorkflowConductorTest):

    @classmethod
    def setUpClass(cls):
        cls.composer_name = 'mistral'
        super(CyclicWorkflowConductorTest, cls).setUpClass()

    def test_cycle(self):
        wf_name = 'cycle'

        expected_wf_graph = {
            'directed': True,
            'graph': {},
            'nodes': [
                {
                    'id': 'prep'
                },
                {
                    'id': 'task1'
                },
                {
                    'id': 'task2'
                },
                {   
                    'id': 'task3'
                }
            ],
            'adjacency': [
                [
                    {
                        'id': 'task1',
                        'criteria': self._get_seq_expr(
                            'prep',
                            states.SUCCESS
                        )
                    }
                ],
                [
                    {
                        'id': 'task2',
                        'criteria': self._get_seq_expr(
                            'task1',
                            states.SUCCESS
                        )
                    }
                ],
                [
                    {
                        'id': 'task3',
                        'criteria': self._get_seq_expr(
                            'task2',
                            states.SUCCESS
                        )
                    }
                ],
                [
                    {
                        'id': 'task1',
                        'criteria': self._get_seq_expr(
                            'task3',
                            states.SUCCESS,
                            "$.count < 3"
                        )
                    }
                ]
            ],
            'multigraph': False
        }

        self._assert_wf_graph(wf_name, expected_wf_graph)

        expected_wf_ex_graph = {
            'directed': True,
            'graph': {},
            'nodes': [
                {
                    'id': 'prep',
                    'name': 'prep'
                },
                {
                    'id': 'task1',
                    'name': 'task1'
                },
                {
                    'id': 'task2',
                    'name': 'task2'
                },
                {
                    'id': 'task3',
                    'name': 'task3'
                }
            ],
            'adjacency': [
                [
                    {
                        'id': 'task1',
                        'criteria': self._get_seq_expr(
                            'prep',
                            states.SUCCESS
                        )
                    }
                ],
                [
                    {
                        'id': 'task2',
                        'criteria': self._get_seq_expr(
                            'task1',
                            states.SUCCESS
                        )
                    }
                ],
                [
                    {
                        'id': 'task3',
                        'criteria': self._get_seq_expr(
                            'task2',
                            states.SUCCESS
                        )
                    }
                ],
                [
                    {
                        'id': 'task1',
                        'criteria': self._get_seq_expr(
                            'task3',
                            states.SUCCESS,
                            "$.count < 3"
                        )
                    }
                ]
            ],
            'multigraph': False
        }

        self._assert_compose(wf_name, expected_wf_ex_graph)

        expected_task_seq = [
            'prep',
            'task1',
            'task2',
            'task3',
            'task1',
            'task2',
            'task3',
            'task1',
            'task2',
            'task3'
        ]

        contexts = [
            {'count': 0},   # prep
            {'count': 0},   # task1
            {'count': 0},   # task2
            {'count': 1},   # task3
            {'count': 1},   # task1
            {'count': 1},   # task2
            {'count': 2},   # task3
            {'count': 2},   # task1
            {'count': 2},   # task2
            {'count': 3}    # task3
        ]

        self._assert_conduct(
            expected_wf_ex_graph,
            expected_task_seq,
            contexts=contexts
        )

    def test_cycles(self):
        wf_name = 'cycles'

        expected_wf_graph = {
            'directed': True,
            'graph': {},
            'nodes': [
                {
                    'id': 'prep'
                },
                {
                    'id': 'task1'
                },
                {
                    'id': 'task2'
                },
                {   
                    'id': 'task3'
                },
                {
                    'id': 'task4'
                },
                {
                    'id': 'task5'
                }
            ],
            'adjacency': [
                [
                    {
                        'id': 'task1',
                        'criteria': self._get_seq_expr(
                            'prep',
                            states.SUCCESS
                        )
                    }
                ],
                [
                    {
                        'id': 'task2',
                        'criteria': self._get_seq_expr(
                            'task1',
                            states.SUCCESS
                        )
                    }
                ],
                [
                    {
                        'id': 'task3',
                        'criteria': self._get_seq_expr(
                            'task2',
                            states.SUCCESS,
                            'not $.proceed'
                        )
                    },
                    {
                        'id': 'task5',
                        'criteria': self._get_seq_expr(
                            'task2',
                            states.SUCCESS,
                            '$.proceed'
                        )
                    }
                ],
                [
                    {
                        'id': 'task4',
                        'criteria': self._get_seq_expr(
                            'task3',
                            states.SUCCESS
                        )
                    }
                ],
                [
                    {
                        'id': 'task2',
                        'criteria': self._get_seq_expr(
                            'task4',
                            states.SUCCESS
                        )
                    }
                ],
                [
                    {
                        'id': 'task1',
                        'criteria': self._get_seq_expr(
                            'task5',
                            states.SUCCESS,
                            "$.count < 3"
                        )
                    }
                ]
            ],
            'multigraph': False
        }

        self._assert_wf_graph(wf_name, expected_wf_graph)

        expected_wf_ex_graph = {
            'directed': True,
            'graph': {},
            'nodes': [
                {
                    'id': 'prep',
                    'name': 'prep'
                },
                {
                    'id': 'task1',
                    'name': 'task1'
                },
                {
                    'id': 'task2',
                    'name': 'task2'
                },
                {
                    'id': 'task3',
                    'name': 'task3'
                },
                {
                    'id': 'task4',
                    'name': 'task4'
                },
                {
                    'id': 'task5',
                    'name': 'task5'
                }
            ],
            'adjacency': [
                [
                    {
                        'id': 'task1',
                        'criteria': self._get_seq_expr(
                            'prep',
                            states.SUCCESS
                        )
                    }
                ],
                [
                    {
                        'id': 'task2',
                        'criteria': self._get_seq_expr(
                            'task1',
                            states.SUCCESS
                        )
                    }
                ],
                [
                    {
                        'id': 'task3',
                        'criteria': self._get_seq_expr(
                            'task2',
                            states.SUCCESS,
                            'not $.proceed'
                        )
                    },
                    {
                        'id': 'task5',
                        'criteria': self._get_seq_expr(
                            'task2',
                            states.SUCCESS,
                            '$.proceed'
                        )
                    }
                ],
                [
                    {
                        'id': 'task4',
                        'criteria': self._get_seq_expr(
                            'task3',
                            states.SUCCESS
                        )
                    }
                ],
                [
                    {
                        'id': 'task2',
                        'criteria': self._get_seq_expr(
                            'task4',
                            states.SUCCESS
                        )
                    }
                ],
                [
                    {
                        'id': 'task1',
                        'criteria': self._get_seq_expr(
                            'task5',
                            states.SUCCESS,
                            "$.count < 3"
                        )
                    }
                ]
            ],
            'multigraph': False
        } 

        self._assert_compose(wf_name, expected_wf_ex_graph)

        expected_task_seq = [
            'prep',
            'task1',
            'task2',
            'task3',
            'task4',
            'task2',
            'task5',
            'task1',
            'task2',
            'task3',
            'task4',
            'task2',
            'task5',
            'task1',
            'task2',
            'task3',
            'task4',
            'task2',
            'task5'
        ]

        contexts = [
            {'count': 0},                   # prep
            {'count': 0, 'proceed': False}, # task1
            {'count': 0, 'proceed': False}, # task2
            {'count': 0, 'proceed': False}, # task3
            {'count': 0, 'proceed': True},  # task4
            {'count': 0, 'proceed': True},  # task2
            {'count': 1, 'proceed': True},  # task5
            {'count': 1, 'proceed': False}, # task1
            {'count': 1, 'proceed': False}, # task2
            {'count': 1, 'proceed': False}, # task3
            {'count': 1, 'proceed': True},  # task4
            {'count': 1, 'proceed': True},  # task2
            {'count': 2, 'proceed': True},  # task5
            {'count': 2, 'proceed': False}, # task1
            {'count': 2, 'proceed': False}, # task2
            {'count': 2, 'proceed': False}, # task3
            {'count': 2, 'proceed': True},  # task4
            {'count': 2, 'proceed': True},  # task2
            {'count': 3, 'proceed': True}   # task5
        ]

        self._assert_conduct(
            expected_wf_ex_graph,
            expected_task_seq,
            contexts=contexts
        )
