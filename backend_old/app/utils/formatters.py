def format_error_response(message, status_code):
    return {'error': True, 'message': message, 'status_code': status_code}, status_code

def format_match_results(matches):
    formatted = []
    for m in matches:
        conf = m['confidence']
        recommendation = (
            "Excellent match" if conf >= 90 else
            "Good match" if conf >= 75 else
            "Moderate match" if conf >= 60 else
            "Low match"
        )
        formatted.append({
            'trial': m['trial'].to_dict(),
            'confidence': f"{conf:.1f}%",
            'reasons': m['reasons'],
            'recommendation': recommendation
        })
    return {'count': len(formatted), 'matches': formatted}
