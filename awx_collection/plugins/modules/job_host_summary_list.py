#!/usr/bin/python
# coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ['preview'], 'supported_by': 'community'}


DOCUMENTATION = '''
---
module: job_host_summary
author: "Scott Harwell (@scottharwell)"
short_description: List job host summaries for a job.
description:
    - List job host summaries for a job. See
      U(https://www.ansible.com/tower) for an overview.
options:
    job_id:
      description:
        - The job ID to retrieve job statuses for.
      type: int
    page:
      description:
        - Page number of the results to fetch.
      type: int
    all_pages:
      description:
        - Fetch all the pages and return a single result.
      type: bool
      default: 'no'
    query:
      description:
        - Query used to further filter the list of jobs. C({"foo":"bar"}) will be passed at C(?foo=bar)
      type: dict
extends_documentation_fragment: awx.awx.auth
'''


EXAMPLES = '''
- name: Get job host summaries
  awx.awx.job_host_summary_list:
    job_id: 12345
  register: job_summaries
'''

RETURN = '''
count:
    description: Total count of objects return
    returned: success
    type: int
    sample: 51
next:
    description: next page available for the listing
    returned: success
    type: int
    sample: 3
previous:
    description: previous page available for the listing
    returned: success
    type: int
    sample: 1
results:
    description: a list of job summary objects represented as dictionaries
    returned: success
    type: list
    sample: [[{"id":1119,"type":"job_host_summary","url":"/api/v2/job_host_summaries/1119/","related":{"job":"/api/v2/jobs/1494/","host":"/api/v2/hosts/16/"},"summary_fields":{"host":{"id":16,"name":"automation_host","description":"imported"},"job":{"id":1494,"name":"Update Hosts","description":"Update Hosts","status":"successful","failed":false,"elapsed":79.149,"type":"job","job_template_id":31,"job_template_name":"Update Hosts"}},"created":"2024-06-21T03:32:13.773492Z","modified":"2024-06-21T03:32:13.773503Z","job":1494,"host":16,"constructed_host":null,"host_name":"automation_host","changed":0,"dark":0,"failures":0,"ok":17,"processed":1,"skipped":23,"failed":false,"ignored":0,"rescued":0}, ...]
'''


from ..module_utils.controller_api import ControllerAPIModule


def main():
    # Any additional arguments that are not fields of the item can be added here
    argument_spec = dict(
        job_id=dict(type='int'),
        page=dict(type='int'),
        all_pages=dict(type='bool', default=False),
        query=dict(type='dict'),
    )

    # Create a module for ourselves
    module = ControllerAPIModule(
        argument_spec=argument_spec
    )

    # Extract our parameters
    job_id = module.params.get('job_id')
    query = module.params.get('query')
    page = module.params.get('page')
    all_pages = module.params.get('all_pages')

    job_search_data = {}
    if page:
        job_search_data['page'] = page
    if query:
        job_search_data.update(query)
    if all_pages:
        job_host_summary = module.get_all_endpoint(f'jobs/{job_id}/job_host_summaries', **{'data': job_search_data})
    else:
        job_host_summary = module.get_endpoint(f'jobs/{job_id}/job_host_summaries', **{'data': job_search_data})

    # Attempt to look up jobs based on the status
    module.exit_json(**job_host_summary['json'])


if __name__ == '__main__':
    main()
