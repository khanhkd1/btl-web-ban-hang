from libraries.connect_database import connect_database, VisitsLog
from datetime import date

session = connect_database()


def track_visitor(request):
	session_tmp = session()
	if request.referrer is None:
		return
	session_tmp.add(
		VisitsLog(
			ip_address=request.remote_addr,
			requested_url=request.url,
            referer_page=request.referrer,
            page_name=request.path,
            query_string=request.query_string,
            user_agent=request.user_agent.string,
            date=str(date.today())
		)
	)
	session_tmp.commit()
	session_tmp.close()
