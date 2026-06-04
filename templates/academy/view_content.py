{% extends 'base.html' %}

{% block title %}{{ content.title }}{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <h4>{{ content.title }}</h4>
        <small>دوره: {{ content.course.title }}</small>
    </div>
    <div class="card-body">
        {% if content.content_type == 'PDF' and content.file %}
            <embed src="{{ content.file.url }}" type="application/pdf" width="100%" height="600px" />
        {% elif content.content_type == 'Video' and content.file %}
            <video width="100%" controls>
                <source src="{{ content.file.url }}" type="video/mp4">
                مرورگر شما از ویدئو پشتیبانی نمی‌کند.
            </video>
        {% elif content.content_type == 'Text' %}
            <div class="border p-3 bg-light">
                {{ content.text_content|linebreaks }}
            </div>
        {% else %}
            <p>فایل موجود نیست یا فرمت پشتیبانی نمی‌شود.</p>
        {% endif %}
    </div>
    <div class="card-footer">
        <a href="{% url 'course_detail' content.course.slug %}" class="btn btn-secondary">بازگشت به دوره</a>
    </div>
</div>
{% endblock %}