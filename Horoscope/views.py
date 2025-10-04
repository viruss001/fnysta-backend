# views.py

from groq import Groq
import json
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import  timedelta,date
from .models import Horo,WeekHoro,MonthHoro,YearHoro
from calendar import monthrange

  # import your LLaMA client
import logging
client = Groq(api_key="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")
logger = logging.getLogger(__name__)


def extract_json_from_text(text):
    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        json_str = text[start:end]
        # remove control characters
        json_str = "".join(ch for ch in json_str if ord(ch) >= 32)
        return json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Cannot parse JSON: {e}")

@api_view(["POST"])
def astroapp_today_api(request):
    zodiac_sign = request.data.get("zodiac_sign", "").lower().strip()
    if not zodiac_sign:
        return Response({"error": "zodiac_sign is required"}, status=status.HTTP_400_BAD_REQUEST)

    today_date = datetime.now().date()

    # Check if horoscope for today already exists
    try:
        existing_entry = Horo.objects.get(sign=zodiac_sign, date=today_date)
        return Response(json.loads(existing_entry.horoscope))
    except Horo.DoesNotExist:
        existing_entry = None

    # Generate prompt for LLaMA
    prompt = f"""
You are my personal Horoscoper.

Write today's horoscope for the zodiac sign "{zodiac_sign}" in english.

Please provide the horoscope in the following detailed format:

- "gnrlhoro": General horoscope with more than 2-3 sentences (4-5 sentences preferred).
- "lovelife": Love life description in 3-4 sentences.
- "business_career": Business and career advice in 2 or 3 lines.
- "student": A brief 1-line note for students.
- "whatdo": Two sentences advising what should be done (क्या करें).
- "whatnotdo": Two sentences advising what should be avoided (क्या न करें).
- "luckyclr": One or two words in decent Hindi indicating lucky color(s).
- "remedy": 2-3 lines with today's special उपाय (remedy).

Respond only with valid JSON like this:

{{
  "gnrlhoro": ["...","...","...","...","..."],
  "lovelife": ["...","...","...","..."],
  "business_career": ["..."],
  "student": ["..."],
  "whatdo": ["...","..."],
  "whatnotdo": ["...","..."],
  "luckyclr": ["...","..."],
  "remedy": ["...","...", "..."]
}}
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant"
        )
        content = chat_completion.choices[0].message.content.strip()
        response_json = extract_json_from_text(content)

        # Store in DB
        if existing_entry:
            existing_entry.horoscope = json.dumps(response_json)
            existing_entry.save()
        else:
            Horo.objects.create(sign=zodiac_sign, horoscope=json.dumps(response_json))

        return Response(response_json)

    except Exception as e:
        logger.error(f"Error in /astroapp: {e}", exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["POST"])
def astroapp_week_api(request):
    zodiac_sign = request.data.get("zodiac_sign", "").lower().strip()
    if not zodiac_sign:
        return Response({"error": "zodiac_sign is required"}, status=status.HTTP_400_BAD_REQUEST)

    today = datetime.now().date()
    # Monday of current week
    week_start = today - timedelta(days=today.weekday())
    # Saturday of current week
    week_end = week_start + timedelta(days=5)

    # 1️⃣ Check if weekly horoscope is already stored
    try:
        existing_entry = WeekHoro.objects.get(zodiac_sign=zodiac_sign, week_start=week_start)
        return Response(existing_entry.horoscope)
    except WeekHoro.DoesNotExist:
        existing_entry = None

    # 2️⃣ Generate weekly prompt for 6 days (Mon → Sat)
    prompt = f"""
You are my personal Horoscoper.

Write the horoscope for the zodiac sign "{zodiac_sign}" from {week_start} to {week_end} (Monday to Saturday) in English.

Provide the horoscope in JSON format, where each array contains individual sentences (no long paragraphs):

- "gnrlhoro": List of sentences describing general horoscope for the week.
- "lovelife": List of sentences describing love life for the week.
- "business_career": List of sentences describing career/business advice.
- "student": List of sentences for students.
- "whatdo": List of 2 sentences advising what should be done (क्या करें).
- "whatnotdo": List of 2 sentences advising what should be avoided (क्या न करें).
- "luckyclr": List of 1-2 words indicating lucky colors .
- "remedy": List of 2-3 sentences with today's special उपाय (remedy).

Example output format:

{{
  "gnrlhoro": ["sentence1", "sentence2", "sentence3", "..."],
  "lovelife": ["sentence1", "sentence2", "..."],
  "business_career": ["sentence1", "sentence2", "..."],   
  "student": ["sentence1", "sentence2", "..."],
  "whatdo": ["sentence1","sentence2"],
  "whatnotdo": ["sentence1","sentence2"],
  "luckyclr": ["color1","color2"],
  "remedy": ["sentence1","sentence2","sentence3"]
}}

Please strictly follow this JSON format and output only valid JSON.
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant"
        )
        content = chat_completion.choices[0].message.content.strip()
        response_json = extract_json_from_text(content)

        # 3️⃣ Store in DB
        WeekHoro.objects.create(
            zodiac_sign=zodiac_sign,
            week_start=week_start,
            week_end=week_end,
            horoscope=response_json
        )

        return Response(response_json)

    except Exception as e:
        logger.error(f"Error in /astroapp_week: {e}", exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["POST"])
def astroapp_month_api(request):
    zodiac_sign = request.data.get("zodiac_sign", "").lower().strip()
    month_str = request.data.get("month")  # optional, format YYYY-MM

    if not zodiac_sign:
        return Response({"error": "zodiac_sign is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Determine month start and end
    try:
        if month_str:
            year, month = map(int, month_str.split("-"))
            month_start = date(year, month, 1)
        else:
            today = datetime.now().date()
            month_start = date(today.year, today.month, 1)
        last_day = monthrange(month_start.year, month_start.month)[1]
        month_end = date(month_start.year, month_start.month, last_day)
    except Exception:
        return Response({"error": "Invalid month format. Use YYYY-MM."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if horoscope exists
    try:
        existing_entry = MonthHoro.objects.get(zodiac_sign=zodiac_sign, month_start=month_start)
        return Response(existing_entry.horoscope)
    except MonthHoro.DoesNotExist:
        existing_entry = None

    # Generate prompt for monthly horoscope
    prompt = f"""
You are my personal Horoscoper.

Write the horoscope for the zodiac sign "{zodiac_sign}" for the month {month_start.strftime('%B %Y')} in english.

Provide the horoscope in JSON format where each array contains individual sentences:

- "gnrlhoro": General horoscope sentences
- "lovelife": Love life sentences
- "business_career": Career/business advice sentences
- "student": Advice for students
- "whatdo": 2 sentences advising what should be done (क्या करें)
- "whatnotdo": 2 sentences advising what should be avoided (क्या न करें)
- "luckyclr": 1-2 words for lucky colors in Hindi
- "remedy": 2-3 sentences with special उपाय

Respond strictly with valid JSON like:

{{
  "gnrlhoro": ["sentence1","sentence2",...],
  "lovelife": ["sentence1","sentence2",...],
  "business_career": ["sentence1","sentence2",...],
  "student": ["sentence1",...],
  "whatdo": ["sentence1","sentence2"],
  "whatnotdo": ["sentence1","sentence2"],
  "luckyclr": ["color1","color2"],
  "remedy": ["sentence1","sentence2","sentence3"]
}}
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant"
        )

        content = chat_completion.choices[0].message.content.strip()
        response_json = extract_json_from_text(content)

        # Store in DB
        MonthHoro.objects.create(
            zodiac_sign=zodiac_sign,
            month_start=month_start,
            month_end=month_end,
            horoscope=response_json
        )

        return Response(response_json)

    except Exception as e:
        logger.error(f"Error in /astroapp_month: {e}", exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["POST"])
def astroapp_year_api(request):
    zodiac_sign = request.data.get("zodiac_sign", "").lower().strip()
    year = request.data.get("year")  # optional

    if not zodiac_sign:
        return Response({"error": "zodiac_sign is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Determine year
    try:
        year = int(year) if year else datetime.now().year
    except Exception:
        return Response({"error": "Invalid year format"}, status=status.HTTP_400_BAD_REQUEST)

    # Check if yearly horoscope exists
    try:
        existing_entry = YearHoro.objects.get(zodiac_sign=zodiac_sign, year=year)
        return Response(existing_entry.horoscope)
    except YearHoro.DoesNotExist:
        existing_entry = None

    # Generate prompt for yearly horoscope
    prompt = f"""
You are my personal Horoscoper.

Write the horoscope for the zodiac sign "{zodiac_sign}" for the year {year} in english.

Provide the horoscope in JSON format where each array contains individual sentences:

- "gnrlhoro": General horoscope sentences
- "lovelife": Love life sentences
- "business_career": Career/business advice sentences
- "student": Advice for students
- "whatdo": 2 sentences advising what should be done (क्या करें)
- "whatnotdo": 2 sentences advising what should be avoided (क्या न करें)
- "luckyclr": 1-2 words for lucky colors in Hindi
- "remedy": 2-3 sentences with special उपाय

Respond strictly with valid JSON like:

{{
  "gnrlhoro": ["sentence1","sentence2",...],
  "lovelife": ["sentence1","sentence2",...],
  "business_career": ["sentence1","sentence2",...],
  "student": ["sentence1",...],
  "whatdo": ["sentence1","sentence2"],
  "whatnotdo": ["sentence1","sentence2"],
  "luckyclr": ["color1","color2"],
  "remedy": ["sentence1","sentence2","sentence3"]
}}
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant"
        )

        content = chat_completion.choices[0].message.content.strip()
        response_json = extract_json_from_text(content)

        # Store in DB
        YearHoro.objects.create(
            zodiac_sign=zodiac_sign,
            year=year,
            horoscope=response_json
        )

        return Response(response_json)

    except Exception as e:
        logger.error(f"Error in /astroapp_year: {e}", exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)