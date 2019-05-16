# Copyright © 2019 Province of British Columbia
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

"""Tests to assure the ops end-point.

Test-Suite to ensure that the /ops endpoint is working as expected.
"""

import json

from registry_schemas import validate_schema
from tests import oracle_integration


@oracle_integration
def test_get_ar(client):
    """Assert that the business info for regular (not xpro) business is correct to spec."""
    rv = client.get('/api/v1/businesses/CP0001965/filings/annual_report')

    assert 200 == rv.status_code
    is_valid, errors = validate_schema(rv.json, 'legal_filings.json')
    if errors:
        for err in errors:
            print('\nERROR MESSAGE:')
            print(err.message)

    assert is_valid


@oracle_integration
def test_get_ar_no_results(client):
    """Assert that the business info for regular (not xpro) business is correct to spec."""
    rv = client.get('/api/v1/businesses/CP0000000/filings/annual_report')

    assert 404 == rv.status_code


@oracle_integration
def test_get_ar_by_year(client):
    """Test getting an AR by year."""
    rv = client.get('/api/v1/businesses/CP0001965/filings/annual_report?year=2015')

    assert 200 == rv.status_code
    is_valid, errors = validate_schema(rv.json, 'legal_filings.json')
    if errors:
        for err in errors:
            print('\nERROR MESSAGE:')
            print(err.message)

    assert is_valid


@oracle_integration
def test_get_ar_by_year_invalid(client):
    """Assert that the business info for regular (not xpro) business is correct to spec."""
    rv = client.get('/api/v1/businesses/CP0001965/filings/annual_report?year=BLA')

    assert 500 == rv.status_code


@oracle_integration
def test_post_ar(client):
    """Assert that the business info for regular (not xpro) business is correct to spec."""
    headers = {'content-type': 'application/json'}

    fake_filing = {
        "filing": {
            "annual_report": {
                "annual_general_meeting_date": "2017-11-23",
                "certified_by": "Joe Smith",
                "email": "nobody@nothing.com"
            },
            "business_info": {
                "last_ledger_timestamp": "2019-05-08T21:21:01-00:00",
                "founding_date": "2004-04-28",
                "identifier": "CP0001965",
                "legal_name": "CENTRAL INTERIOR COMMUNITY SERVICES CO-OP",
                "business_number": None,
                "corp_frozen_typ_cd": None,
                "jurisdiction": "BC",
                "last_agm_date": "2017-11-07",
                "last_ar_filed_date": "2017-04-28",
                "status": "Active",
                "type": "CP"
            },
            "header": {
                "date": "2017-11-23",
                "name": "annual_report"
            }
        }
    }
    rv = client.post('/api/v1/businesses/CP0001965/filings/annual_report',
                     data=json.dumps(fake_filing), headers=headers)

    assert 200 == rv.status_code
    is_valid, errors = validate_schema(rv.json, 'legal_filings.json')
    if errors:
        for err in errors:
            print('\nERROR MESSAGE:')
            print(err.message)

    assert is_valid


@oracle_integration
def test_post_ar_with_invalid_data(client):
    """Assert that the AR post validates correct data before proceeding."""
    headers = {'content-type': 'application/json'}

    fake_filing = {
        "filing": {
            "annual_report": {
                "annual_general_meeting_date": "2017-11-23",
                "certified_by": "Joe Smith",
                "email": "nobody@nothing.com"
            },
            "business_info": {
            },
            "header": {
                "date": "2017-11-23",
                "name": "annual_report"
            }
        }
    }
    rv = client.post('/api/v1/businesses/CP0001965/filings/annual_report',
                     data=json.dumps(fake_filing), headers=headers)

    assert 400 == rv.status_code
    assert 'Error: Invalid Filing schema' == rv.json['message']


@oracle_integration
def test_post_ar_with_mismatched_identifer(client):
    """Assert that the identifier (corp num) must match between URL and posted data."""
    headers = {'content-type': 'application/json'}

    fake_filing = {
        "filing": {
            "annual_report": {
                "annual_general_meeting_date": "2017-11-23",
                "certified_by": "Joe Smith",
                "email": "nobody@nothing.com"
            },
            "business_info": {
                "last_ledger_timestamp": "2019-05-08T21:21:01-00:00",
                "founding_date": "2004-04-28",
                "identifier": "CP0001965",
                "legal_name": "CENTRAL INTERIOR COMMUNITY SERVICES CO-OP",
                "business_number": None,
                "corp_frozen_typ_cd": None,
                "jurisdiction": "BC",
                "last_agm_date": "2017-11-07",
                "last_ar_filed_date": "2017-04-28",
                "status": "Active",
                "type": "CP"
            },
            "header": {
                "date": "2017-11-23",
                "name": "annual_report"
            }
        }
    }
    rv = client.post('/api/v1/businesses/CP0001966/filings/annual_report',
                     data=json.dumps(fake_filing), headers=headers)

    assert 400 == rv.status_code
    assert 'Error: Identifier in URL does not match identifier in filing data' == rv.json['message']