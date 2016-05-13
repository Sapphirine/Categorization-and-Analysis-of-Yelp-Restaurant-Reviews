class Settings:
    def __init__(self):
        pass

    DATASET_FILE = 'yelp_academic_dataset_review.json'
    DATASET_FILE2 = 'yelp_academic_dataset_business.json'

    MONGO_CONNECTION = "mongodb://localhost:27017/"
    REVIEW_DATABASE = "Yelp DB"
    REVIEW_COLLECTION = "Reviews"
    TEST_COLLECTION = "Restaurants"
    LEMMA_COLLECTION = "Lemma"
