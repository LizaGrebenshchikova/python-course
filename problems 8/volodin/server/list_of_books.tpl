<html>
<title>
</title>
<body>
	Книги автора: {{author}}.
	<ul>
	%for book in list_books:
		<li><a href="./book/{{book}}/">{{book}}</a></li>
	%end
	</ul>
</body>
</html>
