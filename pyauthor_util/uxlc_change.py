def uxlc_change(release, change_id):
    return (
        f"https://tanach.us/Changes/{release}%20-%20Changes/"
        + f"{release}%20-%20Changes.xml?"
        + f"{change_id}"
    )
