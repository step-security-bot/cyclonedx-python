# encoding: utf-8

# This file is part of CycloneDX Python Lib
#
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
#
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) OWASP Foundation. All Rights Reserved.

import os
from unittest import TestCase

from cyclonedx_py.parser.poetry import PoetryFileParser


class TestPoetryParser(TestCase):

    def test_simple(self) -> None:
        tests_poetry_lock_file = os.path.join(os.path.dirname(__file__), 'fixtures/poetry-lock-simple.txt')

        parser = PoetryFileParser(poetry_lock_filename=tests_poetry_lock_file)
        self.assertEqual(1, parser.component_count())
        component = next(filter(lambda c: c.name == 'toml', parser.get_components()), None)
        self.assertIsNotNone(component)
        self.assertEqual('toml', component.name)
        self.assertNotEqual(component.purl.to_string(), component.bom_ref.value)
        self.assertEqual('0.10.2', component.version)
        self.assertEqual(2, len(component.external_references), f'{component.external_references}')

    def test_simple_purl_bom_ref(self) -> None:
        tests_poetry_lock_file = os.path.join(os.path.dirname(__file__), 'fixtures/poetry-lock-simple.txt')

        parser = PoetryFileParser(poetry_lock_filename=tests_poetry_lock_file, use_purl_bom_ref=True)
        self.assertEqual(1, parser.component_count())
        component = next(filter(lambda c: c.name == 'toml', parser.get_components()), None)
        self.assertIsNotNone(component)
        self.assertEqual('toml', component.name)
        self.assertEqual(component.purl.to_string(), component.bom_ref.value)
        self.assertEqual('0.10.2', component.version)
        self.assertEqual(2, len(component.external_references), f'{component.external_references}')
