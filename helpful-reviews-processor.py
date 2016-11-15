import argparse
import logging
import time
import shutil
import os
import csv
import statistics

def get_subdirectories(rootdir):
    return [x[0] for x in os.walk(rootdir)]

# Creates a directory for a session
def create_session_directory(directory_name):
    # Build directory name
    directory_path = os.getcwd() + '/helpfuls/' + directory_name

    logger.info('STARTED: Creation of directory ' + os.getcwd() + '/helpfuls/' + directory_name)

    # Create the folder
    os.makedirs(directory_path)

    logger.info('FINISHED: Creation of directory ' + os.getcwd() + '/helpfuls/' + directory_name)

    return directory_path


# Copies review text files from source directory to destination directory
def copy_review_files(source_directory, destination_directory, review_file_names):
    src_files = os.listdir(source_directory)

    for file_name in src_files:
        full_file_name = os.path.join(source_directory, file_name)
        if (os.path.isfile(full_file_name)) and file_name in review_file_names:
            logger.info('STARTED: Copying ' + full_file_name + ' to ' + destination_directory)
            shutil.copy(full_file_name, destination_directory)
            logger.info('FINISHED: Copying ' + full_file_name + ' to ' + destination_directory)


def calculate_lower_and_upper_limit(source_path):
    helpful_votes = list()

    src_files = os.listdir(source_path)
    file_name = ''

    for src_file in src_files:
        if 'reviews' in src_file:
            file_name = src_file
            break

    full_file_name = os.path.join(source_path, file_name)

    logger.info('STARTED: Calculation of helpful votes median, upper and lower limit of ' + full_file_name)
    with open(full_file_name, 'r', encoding='ISO-8859-1') as src_csv:
        reader = csv.DictReader(src_csv, delimiter='|', dialect='excel')

        for row in reader:
            if row['Helpful Votes Count'] != 'n.a.':
                helpful_votes.append(row['Helpful Votes Count'])

    # Sort the list
    helpful_votes = [int(i) for i in helpful_votes]
    helpful_votes.sort()

    for vote in helpful_votes:
        print(vote)

    median = statistics.median(helpful_votes)
    logger.info('INFO: Median is: ' + str(median))

    standard_deviation = statistics.stdev(helpful_votes)

    lower_limit = round(median - standard_deviation, 0)
    upper_limit = round(median + standard_deviation, 0)
    logger.info('INFO: Lower limit is: ' + str(lower_limit))
    logger.info('INFO: Upper limit is: ' + str(upper_limit))
    logger.info('FINISHED: Calculation of helpful votes median, upper and lower limit of ' + full_file_name)

    return [lower_limit, upper_limit]

def calculate_review_file_names(source_path, lower_limit, upper_limit):
    review_file_names = list()

    src_files = os.listdir(source_path)
    file_name = ''

    for src_file in src_files:
        if 'reviews' in src_file:
            file_name = src_file
            break

    full_file_name = os.path.join(source_path, file_name)

    with open(full_file_name, 'r', encoding='ISO-8859-1') as src_csv:
        reader = csv.DictReader(src_csv, delimiter='|', dialect='excel')

        for row in reader:
            if row['Helpful Votes Count'] != 'n.a.' and int(row['Helpful Votes Count']) >= lower_limit and int(row['Helpful Votes Count']) <= upper_limit:
                review_url = row['Review URL']

                occurences_of_dash = [i for i in range(len(review_url)) if review_url.startswith('-', i)]

                review_id = 'review_' + review_url[occurences_of_dash[0] + 1:occurences_of_dash[3]] + '.txt'
                review_file_names.append(review_id)

    return review_file_names


# Main
if __name__ == '__main__':
    # Setup commandline handler
    parser = argparse.ArgumentParser(description='put together helpful reviews selected based on median', usage='python helpful-reviews-processor C:\\Users\\Administrator\\tripadvisor-scrapper\\totalized\\2016-06-01-1522-berlin')
    parser.add_argument('path', help='path of city directory with totalized reviews')
    args = parser.parse_args()

    # Setup logger
    session_timestamp = time.strftime('%Y%m%d-%H%M%S')
    logging.basicConfig(filename='./logs/' + session_timestamp + '-helpful-reviews-processor.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logging.getLogger().addHandler(logging.StreamHandler())

    # Get the source directory path
    source_path = args.path
    source_directory = os.path.basename(os.path.normpath(source_path))

    logger.info('STARTED: Processing of helpful reviews from ' + source_path)

    # Get lower and upper limit
    lower_and_upper_limit = calculate_lower_and_upper_limit(source_path)

    # Get the file names of the reviews whichs helpful votes number lies inbetween lower and upper limit
    review_file_names = calculate_review_file_names(source_path, lower_and_upper_limit[0], lower_and_upper_limit[1])

    # Create the target directory
    target_directory = create_session_directory(source_directory)

    # Get all subdirectory paths of the source directory
    sub_directory_paths = get_subdirectories(source_path)

    # Process each subdirectory
    for sub_directory_path in sub_directory_paths:
        copy_review_files(sub_directory_path, target_directory, review_file_names)

    logger.info('FINISHED: Processing of helpful reviews from ' + source_path)