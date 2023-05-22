from enum import Enum

class ColumnNames(Enum):
    REAL_LOSS_ILS = "הפסד הון"
    REAL_PROFIT_ILS = "רווח הון ריאלי"
    SELL_PRICE_ILS = "תמורה"
    SELL_DATE = "תאריך המכירה"
    ADJUSTED_BUY_PRICE = "מחיר מתואם"
    INDEX_GAIN = "1+ שיעור עליית המדד"
    USD_ILS_SELL_DAY = "שער הדולר ביום המכירה"
    USD_ILS_BUY_DAY = "שער הדולר ביום הקנייה"
    BUY_PRICE_ILS = "מחיר מקורי"
    BUY_PRICE_USD = "ערך נקוב בקניה"
    BUY_DATE = "תאריך הרכישה"
    SELL_PRICE_USD = "ערך נקוב במכירה"
    REGISTERED_PRE_IPO = "נרכש טרם הרישום למסחר"
    SYMBOL = "זיהוי מלא של נייר הערך שנמכר לפי הסדר הכרונולוגי של המכירות"
