def run_skill_assessment(engine):
    """Enhanced assessment using real database questions."""
    from tutorial_mode.database import get_tutorial_db
    
    db = get_tutorial_db()
    
    # Load questions appropriate for user's level
    questions = db.load_questions(difficulty_max=engine.user_skill_profile['level'] + 1)
    
    if not questions:
        # Fallback to hardcoded questions if DB is empty
        questions = [
            {"q": "What is a DDoS attack?", "topic": "basic", "difficulty": 1},
            {"q": "Explain symmetric vs asymmetric encryption.", "topic": "crypto", "difficulty": 2},
        ]
    
    # Present questions and evaluate answers
    print("\n📝 SKILL ASSESSMENT QUIZ")
    print("-" * 40)
    
    score = 0
    for i, q in enumerate(questions[:3], 1):  # Limit to 3 questions for assessment
        print(f"\nQ{i}: {q[1] if isinstance(q, tuple) else q['q']}")
        answer = input("Your answer: ").strip()
        
        # Simple evaluation (in reality, you'd compare with correct_answer)
        if answer:
            score += 1
            print("   ✅ Good effort!")
        else:
            print("   ⚠️  Try to be more specific next time.")
    
    # Update user level based on score
    new_level = min(5, max(1, score))  # Between 1 and 5
    engine.user_skill_profile['level'] = new_level
    
    # Save progress to database
    db.save_user_progress(
        user_id=engine.user_id,
        skill_level=new_level,
        current_module="Assessment Complete",
        progress_data={"assessment_score": score, "questions_attempted": len(questions)}
    )
    
    print(f"\n📊 ASSESSMENT COMPLETE!")
    print(f"   Your level: {new_level}/5")
    print(f"   Score: {score}/3")
    
    return {
        "action": "assessment_complete",
        "score": score,
        "level": new_level,
        "next_state": "LEARNING_PATH_SELECTION",
        "message": f"Assessment complete! You're at level {new_level}. Next: curriculum selection."
    }
