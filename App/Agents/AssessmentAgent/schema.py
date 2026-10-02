from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ChoiceType(str, Enum):
    RADIO = "RADIO"
    CHECKBOX = "CHECKBOX"
    DROP_DOWN = "DROP_DOWN"


class Option(BaseModel):
    value: str = Field(description="نص الخيار المقدم للمستخدم")


class ChoiceQuestion(BaseModel):
    type: ChoiceType = Field(description="نوع سؤال الخيارات: RADIO أو CHECKBOX أو DROP_DOWN")
    options: List[Option] = Field(description="قائمة الخيارات المتاحة")
    shuffle: Optional[bool] = Field(default=False, description="هل يتم خلط الخيارات عشوائياً")


class TextQuestion(BaseModel):
    paragraph: bool = Field(default=False, description="True إذا كانت إجابة طويلة (فقرة)، False إذا كانت إجابة قصيرة")


class ScaleQuestion(BaseModel):
    low: int = Field(default=1, description="الحد الأدنى للمقياس")
    high: int = Field(default=5, description="الحد الأعلى للمقياس")
    low_label: Optional[str] = Field(default=None, description="وصف الحد الأدنى")
    high_label: Optional[str] = Field(default=None, description="وصف الحد الأعلى")


class RatingQuestion(BaseModel):
    rating_scale_level: int = Field(default=5, description="عدد النجوم أو مستويات التقييم")


class Question(BaseModel):
    question_id: Optional[str] = Field(default=None, description="معرف السؤال في حال وجوده")
    required: bool = Field(default=False, description="هل إجابة السؤال إجبارية")
    choice_question: Optional[ChoiceQuestion] = Field(default=None, description="تفاصيل سؤال الخيارات")
    text_question: Optional[TextQuestion] = Field(default=None, description="تفاصيل السؤال النصي")
    scale_question: Optional[ScaleQuestion] = Field(default=None, description="تفاصيل سؤال المقياس المدرج")
    rating_question: Optional[RatingQuestion] = Field(default=None, description="تفاصيل سؤال التقييم")


class Item(BaseModel):
    item_id: Optional[str] = Field(default=None, description="معرف العنصر")
    title: str = Field(description="عنوان السؤال أو العنصر")
    description: Optional[str] = Field(default=None, description="وصف إضافي أو توضيح للسؤال")
    question: Question = Field(description="كائن السؤال وتفاصيله")


class Info(BaseModel):
    title: str = Field(description="عنوان النموذج الرئيسي")
    description: Optional[str] = Field(default=None, description="وصف النموذج الرئيسي")


class QuizSettings(BaseModel):
    is_quiz: bool = Field(default=False, description="هل النموذج عبارة عن اختبار/Quiz")


class FormSettings(BaseModel):
    quiz_settings: Optional[QuizSettings] = Field(default=None, description="إعدادات الاختبارات")


class GoogleFormSchema(BaseModel):
    info: Info = Field(description="المعلومات الأساسية للنموذج")
    settings: Optional[FormSettings] = Field(default=None, description="إعدادات النموذج")
    items: List[Item] = Field(description="قائمة جميع الأسئلة والعناصر المكونة للنموذج")