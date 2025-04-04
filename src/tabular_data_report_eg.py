"""
Example of synthetic data profile report for the Cardio Dataset
"""

from ydata.connectors import GCSConnector
from ydata.metadata.metadata import Metadata
from ydata.report import SyntheticDataProfile
from ydata.synthesizers.regular.model import RegularSynthesizer
from ydata.utils.formats import read_json


def get_token(token_path: str) -> dict:
    "Utility to load a token from .secrets"
    return read_json(token_path)


if __name__ == "__main__":
    # Load the token and read a file from GCS
    gcs_connector = GCSConnector(
        project_id="ydatasynthetic", keyfile_dict=get_token("gcs_credentials.json")
    )

    # Read sample of a .csv file
    data = gcs_connector.read_file("gs://ydata_testdata/tabular/cardio/data.csv")
    metadata = Metadata(data)

    # Train a Synthesizer and sample data
    cardio_synth = RegularSynthesizer()
    cardio_synth.fit(data, metadata=metadata)
    synth_sample = cardio_synth.sample(20_000)

    # get the metadata from the synth, or have an example of how to create a metadata object
    # Generate the Report

    # TODO target variable validation
    profile = SyntheticDataProfile(
        data, synth_sample, metadata=metadata, target="cardio", data_types=cardio_synth.data_types
    )

    profile.generate_report(
        output_path="./cardio_report_example.pdf",
    )
