"""
Lesson and exercise generation crawler
"""
import requests
import re
from loguru import logger

class LessonCrawler:
    def __init__(self):
        self.education_sources = [
            "https://owasp.org/www-project-web-security-testing-guide/",
            "https://portswigger.net/web-security",
            "https://www.hacksplaining.com/lessons",
            "https://tryhackme.com/"
        ]
        logger.info("Lesson Crawler initialized")
    
    def start_crawling(self, intel_queue, bounty_queue, lesson_queue):
        """Crawl for educational content"""
        logger.info("Lesson crawler started")
        while True:
            for source in self.education_sources:
                try:
                    lessons = self.extract_lessons(source)
                    for lesson in lessons:
                        lesson_queue.put({
                            'type': 'lesson_material',
                            'source': source,
                            'lesson': lesson,
                            'difficulty': self.assess_difficulty(lesson['content'])
                        })
                except Exception as e:
                    logger.error(f"Failed to crawl lessons from {source}: {e}")
                time.sleep(60)  # Longer delay for educational content
    
    def extract_lessons(self, url):
        """Extract structured lesson content"""
        response = requests.get(url, timeout=30)
        
        # Look for lesson-like structure
        lessons = []
        if 'owasp' in url:
            # OWASP WSTG specific parsing
            lessons.extend(self.parse_owasp_wstg(response.text))
        elif 'portswigger' in url:
            # PortSwigger specific parsing
            lessons.extend(self.parse_portswigger(response.text))
        
        return lessons
    
    def parse_owasp_wstg(self, html):
        """Parse OWASP Web Security Testing Guide"""
        soup = BeautifulSoup(html, 'html.parser')
        lessons = []
        
        for section in soup.find_all(['h2', 'h3']):
            if 'testing' in section.text.lower() or 'security' in section.text.lower():
                content = section.find_next('p')
                if content:
                    lessons.append({
                        'title': section.text.strip(),
                        'content': content.text[:500] + '...',
                        'category': 'web_security',
                        'source': 'OWASP WSTG'
                    })
        
        return lessons[:10]  # Limit results
