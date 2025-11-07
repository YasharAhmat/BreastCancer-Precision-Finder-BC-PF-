def format_error_response(error,status_code=400):
    return {'error':True,'message':str(error),'status_code':status_code},status_code

def format_match_results(matches):
    return {
        'count':len(matches),
        'matches':[{
            'trial':m['trial'].to_dict(),
            'confidence':f"{m['confidence']:.1f}%",
            'reasons':m['reasons'],
            'recommendation':(
                "Excellent match" if m['confidence']>=90 else
                "Good match" if m['confidence']>=75 else
                "Moderate match" if m['confidence']>=60 else
                "Low match"
            )
        } for m in matches]
    }
