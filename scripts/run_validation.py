from transit_pipeline.validation.validate_warehouse import validate_warehouse

def main():
    print("Starting Adelaide Transit warehouse validation runner..")
    validate_warehouse()
    print("Warehouse validation runner completed successfully.")

if __name__ == "__main__":
    main()