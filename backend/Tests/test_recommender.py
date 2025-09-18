from recommender import Recommender

if __name__ == "__main__":
    total_budget = 700
    build_type = "gaming"  # or "workstation"
    recommender = Recommender("test_builds.db", total_budget, build_type)
    result = recommender.get_recommendations()
    print("\n--- Recommended Build ---")
    for component, details in result["components"].items():
        print(f"{component.upper()}: {details['Name']} - {details['Price']}")
    print(f"\nTotal Price: £{result['total_price']}")