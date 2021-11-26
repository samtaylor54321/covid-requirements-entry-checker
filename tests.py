import pandas as pd
import pytest
import numpy as np
from main import extract_covid_requirements, build_foreign_travel_advice_dataset


@pytest.fixture
def example_html_requirements_present():
    example_text = """<p>The information on this page covers the most common types of travel and reflects the UK government’s understanding of the rules currently in place. Unless otherwise stated, this information is for travellers using a full ‘British Citizen’ passport.</p>\n\n<p>The authorities in the country or territory you’re travelling to are responsible for setting and enforcing the rules for entry. If you’re unclear about any aspect of the entry requirements, or you need further reassurance, you’ll need to contact the <a href="https://www.gov.uk/government/publications/foreign-embassies-in-the-uk">embassy, high commission or consulate</a> of the country or territory you’re travelling to.</p>\n\n<p>You should also consider checking with your transport provider or travel company to make sure your passport and other travel documents meet their requirements.</p>\n\n<h2 id="entry-rules-in-response-to-coronavirus-covid-19">Entry rules in response to coronavirus (COVID-19)</h2>\n\n<h3 id="entry-to-sierra-leone">Entry to Sierra Leone</h3>\n\n<p>From 27 September 2021, all unvaccinated passengers traveling into Sierra Leone will be required to undergo mandatory quarantine at your own cost until you have proof of a negative PCR result.</p>\n\n<p>Before travelling Sierra Leone, you must <a rel="external" href="https://www.travel.gov.sl/">get authorisation from the Government of Sierra Leone through the online portal</a>.</p>\n\n<p>To get authorisation you must have:</p>\n\n<ul>\n  <li>proof of a negative PCR COVID-19 test result no more than 72 hours before the departure time of your flight to Sierra Leone;</li>\n  <li>you should not use the NHS testing service to get a test in order to facilitate your travel to another country. You should arrange to take a private test;</li>\n  <li>a pre-departure public health passenger locator form;</li>\n  <li>and proof of payment for on arrival COVID-19 tests paid for through the portal</li>\n</ul>\n\n<p>Arrivals whose stay in the country does not exceed 5 days do not require to be tested again before leaving the country. However passengers are required to request a certificate of the negative PCR test result that was administered to them when they arrived in Sierra Leone.</p>\n\n<h3 id="testing-on-arrival">Testing on arrival</h3>\n\n<p>On arrival at Freetown Lungi International airport, all passengers are required to have both a COVID-19 PCR and RDT test (in addition to the negative test result required to get authorisation to travel to Sierra Leone). If you test negative for the RDT test, you’ll be allowed to leave the airport and to travel to your final destination, where you must observe public health protocols while you wait for the result of your PCR test (which is expected to take no more than 48 hours). A health locator form with contact details must be completed.</p>\n\n<h3 id="demonstrating-your-covid-19-status">Demonstrating your COVID-19 status</h3>\n\n<p>Sierra Leone has not yet confirmed that it will accept the UK’s proof of COVID-19 recovery and vaccination record.  You should follow the entry rules for unvaccinated people. Your NHS appointment card from vaccination centres is not designed to be used as proof of vaccination.</p>\n\n<h3 id="quarantine-requirements">Quarantine requirements</h3>\n\n<p>If you test positive for the RDT test, you’ll be required to quarantine at a hotel in Lungi at your own expense while you wait for the result of your PCR test. The PCR result supersedes the RDT result. If you test positive for the PCR test result, you’ll be contacted by Sierra Leonean health authorities and required to self-isolate. Passengers sitting in close proximity to a positive case on the flight will be treated as a primary contact and be required to self-isolate until you return a negative PCR COVID-19 test. Social distancing and the use of facemasks is mandatory at Freetown Lungi International airport.</p>\n\n<h3 id="testing-on-departure">Testing on departure</h3>\n\n<p>Before departure from Sierra Leone, you’ll need to <a rel="external" href="https://www.travel.gov.sl/">pay for and take a  PCR COVID-19 test through the portal</a> within 72 hours of your departure. Certificates confirming the test result will be emailed to you. You’ll need to provide this certificate confirming your test result at check-in. If you test positive, you’ll not be allowed to travel and you’ll need to follow public health protocols for isolation and contact tracing.</p>\n\n<p>If your stay in Sierra Leone is for 5 days or less, you are exempt from needing a further test ahead of departure. You’re exempt from the COVID-19 test on departure if you arrived in Sierra Leone fewer than 5 days before departing. Children under two years of age are also exempt.</p>\n\n<p>If you think you have COVID-19 symptoms you should call the Government of Sierra Leone emergency line on 117 (local). Treatment for coronavirus cases is carried out at Government of Sierra Leone facilities.</p>\n\n<p>The <a rel="external" href="https://mohs.gov.sl/covid-19/">Ministry of Health website</a> has additional information.</p>\n\n<h2 id="regular-entry-requirements">Regular entry requirements</h2>\n\n<h3 id="visas">Visas</h3>\n\n<p>You will need a visa to enter Sierra Leone.</p>\n\n<p>Visitors from the UK can get a visa on arrival in Sierra Leone for US$80, which must be paid in cash in US dollars. However, if you’re travelling to Sierra Leone for a purpose other than tourism, a visit or business, you will need to get a visa before you travel. Contact the <a href="https://www.gov.uk/government/publications/foreign-embassies-in-the-uk">Sierra Leonean High Commission in London</a> for details.</p>\n\n<p>The Sierra Leone High Commission in London sometimes issues Emergency Travel Certificates to Sierra Leoneans resident in the UK and those with dual British/Sierra Leone nationality. These documents are not valid for return travel to the UK. Sierra Leone nationals require a visa for the UK, which can only be issued in a full passport.</p>\n\n<h3 id="passport-validity">Passport validity</h3>\n\n<p>Your passport should be valid for a minimum period of 6 months from the time of your visa application.</p>\n\n<h3 id="yellow-fever-certificate-requirements">Yellow fever certificate requirements</h3>\n\n<p>Check whether you need a yellow fever certificate by visiting the National Travel Health Network and Centre’s <a rel="external" href="http://travelhealthpro.org.uk/country/195/sierra-leone#Vaccine_recommendations">TravelHealthPro website</a>.</p>\n\n<h3 id="uk-emergency-travel-documents">UK Emergency Travel Documents</h3>\n\n<p>UK <a href="https://www.gov.uk/emergency-travel-document">Emergency Travel Documents</a> (ETDs) are not valid for entry into Sierra Leone. ETDs are accepted for airside transit and exit from Sierra Leone.</p>\n"""
    return example_text


@pytest.fixture
def example_html_requirements_not_present():
    example_text = """<p>This page reflects the UK government’s understanding of current rules for people travelling on a full ‘British Citizen’ passport, for the most common types of travel.</p>\n\n<p>The authorities in Seychelles set and enforce entry rules. For further information <a href="https://www.gov.uk/government/publications/foreign-embassies-in-the-uk">contact the embassy, high commission or consulate</a> of the country or territory you’re travelling to. You should also consider checking with your transport provider or travel company to make sure your passport and other travel documents meet their requirements.</p>\n\n<h2 id="entry-rules-in-response-to-coronavirus-covid-19">Entry rules in response to coronavirus (COVID-19)</h2>\n\n<p>On 25 March 2021, Seychelles opened its borders to visitors irrespective of their vaccination status. All visitors must present a negative PCR test, taken within 72 hours prior to departure, and must stay in approved accommodation. There will be no quarantine requirement and no restriction on movement for most visitors upon entry to Seychelles. Visitors must adhere to public health measures.</p>\n\n<p>Visitors who have been in Bangladesh, Brazil, India or Pakistan within 14 days prior to travel will not be permitted to enter Seychelles. This list is kept under review.</p>\n\n<p>If you plan to travel to Seychelles, you must do so in accordance with current UK COVID-19 restrictions and  should familiarise yourself with the travel advisory at the <a rel="external" href="http://tourism.gov.sc/covid-19-guidelines/">Ministry for Foreign Affairs and Tourism website</a> and the ‘conditions for entry’ section of the <a rel="external" href="http://www.health.gov.sc/">Ministry of Health website</a>, which outline all requirements for entry and pre-travel conditions which must be met.</p>\n\n<p>An application for entry form should also be completed and returned to the Public Health Authority before travel. Work permit holders must also be cleared by the Department of Employment and Immigration. If you’re uncertain of your status, you should contact the Department of Employment and Immigration before attempting to enter Seychelles.</p>\n\n<p>You can find a travel advisory detailing the full entry procedures for all travellers at the <a rel="external" href="http://tourism.gov.sc/covid-19-guidelines/">Ministry for Foreign Affairs and Tourism website</a> and ‘conditions for entry’ at the <a rel="external" href="http://www.health.gov.sc/">Ministry of Health website</a>.  You’re strongly advised to familiarise yourself with the full entry requirements before you travel.  These may be updated regularly and without warning.</p>\n\n<p>A Health Travel Authorisation is required for travellers entering Seychelles by sea.  Travellers arriving by sea who have spent at least 14 days at sea since their last port of call do not require a PCR test.  Clients or crew who wish to disembark before completion of 14 days since their last port of call must have proof of vaccination and undertake a PCR test on arrival.  If you are travelling by sea, you should follow the guidelines on the ‘conditions for entry’ at the <a rel="external" href="http://www.health.gov.sc/">Ministry of Health website</a>.</p>\n\n<p>Cruise ships from any country worldwide will not be permitted to berth in Seychelles until further notice.</p>\n\n<h3 id="screening-on-arrival">Screening on arrival</h3>\n\n<p>All visitors must present a negative PCR test on arrival, taken within the 72 hours prior to their departure.</p>\n\n<p>All passengers will be temperature checked at all ports of arrival. If symptoms of COVID-19 are found to be present, tests will be conducted. Those found to be positive will be quarantined and re-checked.</p>\n\n<h3 id="quarantine-requirements">Quarantine requirements</h3>\n\n<p>There will be no quarantine requirements and no restriction on movement for most visitors upon entry to Seychelles.</p>\n\n<p>Seychellois nationals and permanent residents may enter Seychelles from any country and will not face quarantine if they have completed a full dose of vaccination at least two weeks before travelling. Unvaccinated Seychellois nationals and permanent residents must undergo 7 days of home quarantine.</p>\n\n<p>Gainful Occupational Permit (GOP) holders may enter Seychelles from any country and will not face quarantine if they have completed a full dose of vaccination at least two weeks before travelling.  All unvaccinated GOP holders travelling to Seychelles will be expected to undergo 7 days of quarantine in a private quarantine facility or a certified tourism establishment.</p>\n\n<p>If you intend to travel to Seychelles, you should familiarise yourself with the ‘conditions for entry’ section of the <a rel="external" href="http://www.health.gov.sc/">Ministry for Health website</a>.</p>\n\n<h3 id="demonstrating-your-covid-19-status">Demonstrating your COVID-19 status</h3>\n\n<p>Seychelles has not yet confirmed that it will accept the UK’s proof of COVID-19 recovery and vaccination record.  You should follow the entry rules for unvaccinated people. Your NHS appointment card from vaccination centres is not designed to be used as proof of vaccination.</p>\n\n<h2 id="regular-entry-requirements">Regular entry requirements</h2>\n\n<p>The Government of Seychelles is reviewing its policies on work permits (Gainful Occupational Permits) for foreign nationals. Following the economic impact of the coronavirus, it is a possibility that Gainful Occupational Permits for some foreign nationals will not be renewed. You should speak to your employer and contact the Government of Seychelles Department for Immigration and Civil Status if you hold a Gainful Occupational Permit and are concerned about your employment status in Seychelles.</p>\n\n<h3 id="visas">Visas</h3>\n\n<p>Visas are not required for British passport holders.</p>\n\n<h3 id="passport-validity">Passport validity</h3>\n\n<p>Your passport should be valid for the proposed duration of your stay. No additional period of validity beyond this is required.</p>\n\n<h3 id="uk-emergency-travel-documents">UK Emergency Travel Documents</h3>\n\n<p>UK Emergency Travel Documents (ETDs) are accepted for entry, airside transit and exit from Seychelles.</p>\n\n<h3 id="yellow-fever-certificate-requirements">Yellow fever certificate requirements</h3>\n\n<p>Check whether you need a yellow fever certificate by visiting the National Travel Health Network and Centre’s <a rel="external" href="http://travelhealthpro.org.uk/country/194/seychelles#Vaccine_recommendations">TravelHealthPro website</a>.</p>\n"""
    return example_text


@pytest.fixture
def example_country_urls():
    example_country_urls = {
        "Greece": "https://www.gov.uk/api/content/foreign-travel-advice/greece",
        "Sweden": "https://www.gov.uk/api/content/foreign-travel-advice/sweden",
        "Thailand": "https://www.gov.uk/api/content/foreign-travel-advice/thailand",
    }
    return example_country_urls


@pytest.fixture
def example_country_urls_malformed():
    example_country_urls_malformed = {
        "Greece": "https://www.gov.uk/api/content/foreign-travel-advice/greece",
        "Sweden": "https://www.gov.uk/api/content/foreign-travel-advice/sweden",
        "Thailand": "This is a missing or malformed url",
    }
    return example_country_urls_malformed


class TestExtractCovidRequirements:
    """Test suite for extracting entry requirements for a given country"""

    def test_extract_covid_requirements_string_present(
        self, example_html_requirements_present
    ):
        """Test to ensure that the correct data is extracted if the text
        is present"""

        # Example string
        example_result = """<h3 id="entry-to-sierra-leone">Entry to Sierra Leone</h3>\n\n<p>From 27 September 2021, all unvaccinated passengers traveling into Sierra Leone will be required to undergo mandatory quarantine at your own cost until you have proof of a negative PCR result.</p>\n\n<p>Before travelling Sierra Leone, you must <a rel="external" href="https://www.travel.gov.sl/">get authorisation from the Government of Sierra Leone through the online portal</a>.</p>\n\n<p>To get authorisation you must have:</p>\n\n<ul>\n  <li>proof of a negative PCR COVID-19 test result no more than 72 hours before the departure time of your flight to Sierra Leone;</li>\n  <li>you should not use the NHS testing service to get a test in order to facilitate your travel to another country. You should arrange to take a private test;</li>\n  <li>a pre-departure public health passenger locator form;</li>\n  <li>and proof of payment for on arrival COVID-19 tests paid for through the portal</li>\n</ul>\n\n<p>Arrivals whose stay in the country does not exceed 5 days do not require to be tested again before leaving the country. However passengers are required to request a certificate of the negative PCR test result that was administered to them when they arrived in Sierra Leone.</p>"""

        # Check that the correct text is extracted from the string
        assert extract_covid_requirements(example_html_requirements_present).replace(
            "\n", ""
        ) == example_result.replace("\n", "")

    def test_extract_covid_requirements_string_not_present(
        self, example_html_requirements_not_present
    ):
        """Test to ensure that the error handling works when there are
        no specified entry requirements"""

        # Check that if the text doesn't contain the string that it's correctly handled.
        assert (
            extract_covid_requirements(example_html_requirements_not_present)
            == "No entry rules in response to coronavirus are listed"
        )


class TestBuildForeignTravelAdviceDataset:
    """Test suite for Build Foreign Travel Advice Dataset function"""

    def test_build_foreign_travel_advice_dataset(self, example_country_urls):
        """Tests that the output of the function is correct when all necessary
        data is present"""

        # Parse test data which contains no errors
        test_data = pd.read_csv("test_data/test_data.csv")

        foreign_advice_dataset = build_foreign_travel_advice_dataset(
            example_country_urls
        )

        # Check that results of the malformed url are processed correctly
        assert np.all(
            foreign_advice_dataset.columns.values == test_data.columns.values
        ) and np.all(foreign_advice_dataset["name"] == test_data["name"])

    def test_build_foreign_travel_advice_data_malformed(
        self, example_country_urls_malformed
    ):
        """Tests the exeception handling for this function when url is missing"""

        # Parse test data with malformed example
        test_data = pd.read_csv("test_data/test_data_malformed.csv")

        # Build foreign advice dataset
        foreign_advice_dataset = build_foreign_travel_advice_dataset(
            example_country_urls_malformed
        )

        # Check that results of the malformed url are processed correctly
        assert np.all(
            foreign_advice_dataset.columns.values == test_data.columns.values
        ) and np.all(foreign_advice_dataset["name"] == test_data["name"])
