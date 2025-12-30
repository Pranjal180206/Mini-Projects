from db_recorder import fetch_all

def main():
    records = fetch_all()

    print("\nSaved Classification Records")
    print("-" * 40)

    for r in records:
        print(
            f"ID: {r[0]} | "
            f"Time: {r[1]} | "
            f"Image: {r[2]} | "
            f"Class: {r[3]} | "
            f"Confidence: {r[4]:.2f}"
        )

if __name__ == "__main__":
    main()
