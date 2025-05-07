from flask import send_from_directory, Flask, jsonify, render_template
from bs4 import BeautifulSoup
from flask_cors import CORS
import re

def clean_rating(text):
    match = re.search(r"\d+", text)
    return match.group() if match else "0"

app = Flask(__name__)
CORS(app, origins=["https://rohandev.online","https://rohan3004.github.io"])

HTML_FILE_PATH = "output.html"

def parse_html_stats():
    with open(HTML_FILE_PATH, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    stats = {}

    # Total Questions and Total Active Days
    card_divs = soup.find_all("div", class_="relative flex flex-col items-center justify-center w-full h-full gap-2 p-4 bg-white border round-border shadow-sm dark:bg-darkBox-900 dark:border-darkBorder-800")
    for card in card_divs:
        label = card.find("div", class_="font-semibold whitespace-nowrap text-center text-gray-500 dark:text-darkText-400")
        value = card.find("span", class_="text-5xl font-sans dark:text-darkText-300 font-extrabold")
        if label and value:
            text = label.text.strip()
            number = value.text.strip()
            if text == "Total Questions":
                stats["total_questions"] = number
            elif text == "Total Active Days":
                stats["total_active_days"] = number

    # Submissions, Max Streak, Current Streak
    streak_section = soup.find("div", class_="flex items-center gap-4 justify-between w-full lg:w-auto")
    if streak_section:
        spans = streak_section.find_all("span")
        if len(spans) >= 6:
            stats["submissions"] = spans[0].text.strip()
            stats["max_streak"] = spans[3].text.strip()
            stats["current_streak"] = spans[5].text.strip()

    # Platform-wise Contest Counts
    contest_block = soup.find("div", id="contest_description")
    if contest_block:
        for li in contest_block.find_all("li"):
            name_span = li.find("span")
            count_span = li.find_all("span")[-1]
            if name_span and count_span:
                name = name_span.text.strip().lower()
                value = count_span.text.strip()
                if "leetcode" in name:
                    stats["leetcode_contests"] = value
                elif "codechef" in name:
                    stats["codechef_contests"] = value
                elif "codeforces" in name:
                    stats["codeforces_contests"] = value

    # Awards
    badges_section = soup.find("div", id="badges")
    if badges_section:
        award_span = badges_section.find("span", class_="-mt-2 text-sm font-bold text-gray-400")
        if award_span:
            stats["awards"] = award_span.text.strip()

    problems_section = soup.find("div", id="problems_solved")
    if problems_section:
        sections = problems_section.find_all("div", recursive=False)[-1].find_all("div", recursive=False)

    # Fundamentals
    fundamentals_block = sections[0]
    fundamentals_total = fundamentals_block.find("span", class_="text-2xl font-extrabold dark:text-darkText-300")
    stats["fundamentals_total"] = fundamentals_total.text.strip() if fundamentals_total else None

    fundamentals_platforms = fundamentals_block.find_all("div",
                                                         class_="flex justify-between p-2 text-sm font-semibold text-gray-600 bg-gray-100 round-border dark:text-darkText-300 dark:bg-darkBox-800")
    for platform in fundamentals_platforms:
        name = platform.find("div").text.strip().lower()
        value = platform.find("span").text.strip()
        stats[f"fundamentals_{name}"] = value

    # DSA
    dsa_block = sections[2]
    dsa_total = dsa_block.find("span", class_="text-2xl font-extrabold dark:text-darkText-300")
    stats["dsa_total"] = dsa_total.text.strip() if dsa_total else None

    dsa_difficulties = dsa_block.find_all("div",
                                          class_="flex justify-between p-2 text-sm font-semibold text-gray-600 bg-gray-100 round-border dark:text-darkText-300 dark:bg-darkBox-800")
    for level in dsa_difficulties:
        name = level.find("div").text.strip().lower()
        value = level.find("span").text.strip()
        stats[f"dsa_{name}"] = value

    # Competitive Programming
    cp_block = sections[4]
    cp_total = cp_block.find("span", class_="text-2xl font-extrabold dark:text-darkText-300")
    stats["competitive_programming_total"] = cp_total.text.strip() if cp_total else None

    cp_platforms = cp_block.find_all("div",
                                     class_="flex justify-between p-2 text-sm font-semibold text-gray-600 bg-gray-100 round-border dark:text-darkText-300 dark:bg-darkBox-800")
    for platform in cp_platforms:
        name = platform.find("div").text.strip().lower()
        value = platform.find("span").text.strip()
        stats[f"competitive_{name}"] = value

    rankings_div = soup.find("div", id="contest_ratings")
    if not rankings_div:
        return stats

    sections = rankings_div.find_all("div", class_="flex-1") + rankings_div.find_all("div", recursive=False)

    # LeetCode
    leetcode_section = rankings_div.find("div", string=lambda x: x and "LEETCODE" in x.upper())
    if leetcode_section:
        leetcode_block = leetcode_section.find_parent()
        current = leetcode_block.find("h3", class_="text-4xl font-bold").text.strip()
        max_text = leetcode_block.find("span").text.strip()
        max_val = max_text.replace("max :", "").replace(")", "").strip()
        max_val = clean_rating(max_val)
        stats["leetcode_contest_rating"] = {"current": current, "max": max_val}

    # CodeChef
    codechef_section = rankings_div.find("div", string=lambda x: x and "CODECHEF" in x.upper())
    if codechef_section:
        codechef_block = codechef_section.find_parent()
        current = codechef_block.find("h3", class_="text-4xl font-bold").text.strip()
        max_text = codechef_block.find("span").text.strip()
        max_val = max_text.replace("max :", "").replace(")", "").strip()
        max_val = clean_rating(max_val)
        stats["codechef_contest_rating"] = {"current": current, "max": max_val}

    # Codeforces
    codeforces_section = rankings_div.find("div", string=lambda x: x and "CODEFORCES" in x.upper())
    if codeforces_section:
        codeforces_block = codeforces_section.find_parent()
        current = codeforces_block.find("h3", class_="text-4xl font-bold").text.strip()
        spans = codeforces_block.find_all("span")
        max_val = spans[0].text.strip().replace("max :", "").replace(")", "").strip()
        max_val = clean_rating(max_val)
        rank = spans[1].text.strip() if len(spans) > 1 else None
        stats["codeforces_contest_rating"] = {
            "current": current,
            "max": max_val,
            "rank": rank
        }

    return stats

@app.route("/stats", methods=["GET"])
def get_stats():
    stats = parse_html_stats()
    return jsonify(stats)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/x-icon')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('404.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
