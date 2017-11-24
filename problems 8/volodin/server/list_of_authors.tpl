<html>
<title>
</title>
<body>
	Авторы и их книги:
	<ul>
	%for author in authors:
		<li><a href="/author/{{author}}/">{{author}}</a></li>
		<ul>
		%for book in books[author]:
			<li><a href="/author/{{author}}/book/{{book}}/">{{book}}</a></li>
		%end
		</ul>
	%end
	</ul>
</body>
</html>
