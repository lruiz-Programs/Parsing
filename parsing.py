import requests
from bs4 import BeautifulSoup


def print_grid_from_google_doc(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')
    if table is None:
        raise ValueError(f"No table found at URL: {url}")

    entries = []
    for row in table.find_all('tr')[1:]:  # skipping header
        cells = row.find_all(['td', 'th'])
        if len(cells) < 3:
            continue
        x_text = cells[0].get_text(strip=True)
        char = cells[1].get_text(strip=True)
        y_text = cells[2].get_text(strip=True)
        try:
            x = int(x_text)
            y = int(y_text)
        except ValueError:
            continue
        entries.append((x, y, char))

    if not entries:
        print("No valid data entries found.")
        return

    max_x = max(x for x, _y, _c in entries)
    max_y = max(y for _x, y, _c in entries)
    width = max_x + 1
    height = max_y + 1

    grid = [[" " for _ in range(width)] for _ in range(height)]

    for x, y, char in entries:
        row = height - y - 1
        col = x
        grid[row][col] = char

    for row_cells in grid:
        print(''.join(row_cells))


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <google_doc_url>")
        sys.exit(1)
    print_grid_from_google_doc(sys.argv[1])

