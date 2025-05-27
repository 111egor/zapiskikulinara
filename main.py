from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Модель базы данных
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)


# Создаем базу и тестовые данные
with app.app_context():
    db.create_all()

    # Удаляем все существующие записи, чтобы избежать дублирования
    db.session.query(Recipe).delete()

    # Добавляем начальные рецепты
    initial_recipes = [
        Recipe(
            title="Классический борщ",
            category="soup",
            ingredients="Свекла, капуста, картофель, морковь, лук, мясо, томатная паста",
            instructions="1. Варим мясной бульон\n2. Обжариваем овощи\n3. Соединяем и варим 40 минут"
        ),
        Recipe(
            title="Грибной суп",
            category="soup",
            ingredients="Грибы, лук, картофель, морковь, сливочное масло, сметана",
            instructions="1. Обжариваем грибы с луком\n2. Добавляем картофель и морковь\n3. Варим 30 минут"
        ),
        Recipe(
            title="Куриный суп",
            category="soup",
            ingredients="Курица, лук, морковь, картофель, лапша",
            instructions="1. Варим курицу\n2. Добавляем овощи\n3. Варим лапшу"
        ),
        Recipe(
            title="Томатный суп",
            category="soup",
            ingredients="Помидоры, лук, морковь, бульон, сливки",
            instructions="1. Обжариваем овощи\n2. Добавляем помидоры и бульон\n3. Варим 20 минут"
        ),
        Recipe(
            title="Суп минестроне",
            category="soup",
            ingredients="Фасоль, помидоры, лук, морковь, макароны",
            instructions="1. Обжариваем овощи\n2. Добавляем фасоль и помидоры\n3. Варим макароны"
        ),
        Recipe(
            title="Гречка с грибами",
            category="main",
            ingredients="Гречка, шампиньоны, лук, масло, соль",
            instructions="1. Варим гречку\n2. Обжариваем грибы с луком\n3. Смешиваем"
        ),
        Recipe(
            title="Картофельное пюре",
            category="main",
            ingredients="Картофель, молоко, сливочное масло, соль",
            instructions="1. Варим картофель\n2. Разминаем и добавляем молоко и масло\n3. Солим"
        ),
        Recipe(
            title="Макароны по-флотски",
            category="main",
            ingredients="Макароны, фарш, лук, томатная паста",
            instructions="1. Варим макароны\n2. Обжариваем фарш с луком\n3. Смешиваем с томатной пастой"
        ),
        Recipe(
            title="Котлеты",
            category="main",
            ingredients="Фарш, лук, яйцо, хлеб, соль, перец",
            instructions="1. Смешиваем фарш с луком и яйцом\n2. Формируем котлеты\n3. Обжариваем"
        ),
        Recipe(
            title="Плов",
            category="main",
            ingredients="Рис, мясо, лук, морковь, специи",
            instructions="1. Обжариваем мясо с луком\n2. Добавляем морковь и рис\n3. Варим"
        ),
        Recipe(
            title="Брускетта с томатами",
            category="snack",
            ingredients="Багет, помидоры, чеснок, оливковое масло, базилик",
            instructions="1. Подсушиваем хлеб\n2. Натираем чесноком\n3. Выкладываем начинку"
        ),
        Recipe(
            title="Канапе с лососем",
            category="snack",
            ingredients="Хлеб, лосось, сливочный сыр, укроп",
            instructions="1. Нарезаем хлеб\n2. Смазываем сливочным сыром\n3. Выкладываем лосось и укроп"
        ),
        Recipe(
            title="Овощные чипсы",
            category="snack",
            ingredients="Свекла, морковь, картофель, масло, соль",
            instructions="1. Нарезаем овощи\n2. Обжариваем в масле\n3. Солим"
        ),
        Recipe(
            title="Сырные палочки",
            category="snack",
            ingredients="Сыр, тесто, яйцо",
            instructions="1. Нарезаем сыр\n2. Заворачиваем в тесто\n3. Обжариваем"
        ),
        Recipe(
            title="Фрукты в шоколаде",
            category="snack",
            ingredients="Фрукты, шоколад",
            instructions="1. Растапливаем шоколад\n2. Обмакиваем фрукты\n3. Охлаждаем"
        ),
        Recipe(
            title="Суп том ям",
            category="exotic",
            ingredients="Креветки, кокосовое молоко, лемонграсс, грибы, чили",
            instructions="1. Варим бульон с лемонграссом\n2. Добавляем остальные ингредиенты\n3. Варим 15 минут"
        ),
        Recipe(
            title="Суши",
            category="exotic",
            ingredients="Рис, нори, рыба, огурец, авокадо",
            instructions="1. Варим рис\n2. Раскатываем нори\n3. Выкладываем начинку"
        ),
        Recipe(
            title="Паэлья",
            category="exotic",
            ingredients="Рис, морепродукты, курица, шафран",
            instructions="1. Обжариваем курицу\n2. Добавляем рис и шафран\n3. Добавляем морепродукты"
        ),
        Recipe(
            title="Такос",
            category="exotic",
            ingredients="Лепешки, мясо, салат, сыр, соус",
            instructions="1. Обжариваем мясо\n2. Нагреваем лепешки\n3. Собираем такос"
        ),
        Recipe(
            title="Лазанья",
            category="exotic",
            ingredients="Тесто, фарш, сыр, томатный соус",
            instructions="1. Готовим фарш\n2. Собираем слои\n3. Запекаем"
        )
    ]
    db.session.add_all(initial_recipes)
    db.session.commit()

# HTML шаблоны
base_template = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}} | Кулинарный сайт</title>
    <style>
       /* Основные стили */
:root {
  --primary-color: #2c3e50;
  --secondary-color: #1abc9c;
  --accent-color: #f1c40f;
  --light-color: #ecf0f1;
  --dark-color: #34495e;
  --text-color: #333;
  --text-light: #7f8c8d;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
   font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      line-height: 1.6;
      color: var(--text-color);
    background-image: url('https://img.freepik.com/free-photo/top-view-cooked-potatoes-delicious-dish-with-greens-dark-surface-cooking-dish-potatoes-dinner-meal-food_140725-101577.jpg?semt=ais_hybrid&w=740');      
    background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      background-attachment: fixed;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
}

.container {
      max-width: 800px; /* Уменьшаем максимальную ширину */
      margin: 2rem auto;
      padding: 1.5rem; /* Уменьшаем внутренние отступы */
      flex: 1;
      background-color: rgba(255, 255, 255, 0.9); /* Более прозрачный фон */
      border-radius: 15px; /* Более скругленные углы */
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Более легкая тень */
      border: 1px solid rgba(0, 0, 0, 0.1); /* Тонкая граница */
    }

/* Шапка сайта */
.header {
  background: linear-gradient(135deg, var(--primary-color), var(--dark-color));
  color: white;
  padding: 1.5rem 0;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: relative;
  overflow: hidden;
}

.header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: var(--secondary-color);
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
}

/* Навигационное меню */
.nav {
  display: flex;
  justify-content: center;
  background-color: var(--dark-color);
  padding: 1rem;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nav a {
  color: var(--light-color);
  padding: 0.5rem 1.5rem;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  margin: 0 0.5rem;
  border-radius: 4px;
  transition: all 0.3s ease;
  position: relative;
}

.nav a:hover {
  color: var(--accent-color);
  transform: translateY(-2px);
}

.nav a::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background: var(--secondary-color);
  transition: width 0.3s ease;
}

.nav a:hover::after {
  width: 70%;
}

/* Основное содержимое */
.container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
  flex: 1;
}

/* Карточки рецептов */
.recipe-card {
  background: white;
  border-radius: 10px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  overflow: hidden;
}

.recipe-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
}

.recipe-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 5px;
  height: 100%;
  background: var(--secondary-color);
}

.recipe-title {
  color: var(--primary-color);
  font-size: 1.8rem;
  margin-bottom: 1rem;
  font-weight: 700;
  border-bottom: 2px solid var(--light-color);
  padding-bottom: 0.5rem;
}

.recipe-section h4 {
  color: var(--dark-color);
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
}

.recipe-section h4::before {
  content: '•';
  color: var(--secondary-color);
  margin-right: 0.5rem;
  font-size: 1.5rem;
}

.recipe-section p {
  margin-left: 1.5rem;
  color: var(--text-color);
}

/* Подвал сайта */
.footer {
  background: linear-gradient(135deg, var(--dark-color), var(--primary-color));
  color: white;
  text-align: center;
  padding: 2rem;
  margin-top: 3rem;
}

.footer p {
  font-size: 1.1rem;
  letter-spacing: 1px;
}

/* Анимации */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.recipe-card {
  animation: fadeIn 0.6s ease forwards;
}

/* Адаптивность */
@media (max-width: 768px) {
  .header h1 {
    font-size: 2rem;
  }

  .nav {
    flex-wrap: wrap;
    padding: 0.5rem;
  }

  .nav a {
    padding: 0.5rem;
    margin: 0.25rem;
    font-size: 1rem;
  }

  .container {
    padding: 0 1rem;
  }

  .recipe-card {
    padding: 1.5rem;
  }

  .recipe-title {
    font-size: 1.5rem;
  }
}

/* Специальные эффекты для экзотических рецептов */
.exotic .recipe-card {
  border: 2px dashed var(--accent-color);
}

.exotic .recipe-title {
  color: var(--accent-color);
}

/* Кнопка "Наверх" */
.scroll-top {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: var(--secondary-color);
  color: white;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 99;
}

.scroll-top.active {
  opacity: 1;
  visibility: visible;
}

.scroll-top:hover {
  background: var(--primary-color);
  transform: translateY(-3px);
}

/* Поисковая строка */
.search-form {
  display: flex;
  justify-content: center;
  margin: 2rem 0;
}

.search-input {
  padding: 0.5rem 1rem;
  width: 60%;
  border: 2px solid var(--secondary-color);
  border-radius: 25px;
  font-size: 1rem;
  outline: none;
}

.search-button {
  padding: 0.5rem 1.5rem;
  background-color: var(--secondary-color);
  color: white;
  border: none;
  border-radius: 25px;
  margin-left: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

.search-button:hover {
  background-color: var(--primary-color);
}

.not-found {
  text-align: center;
  font-size: 1.5rem;
  color: var(--text-light);
  margin: 2rem 0;
}
    </style>
</head>
<body>
    <header class="header">
        <h1>Кулинарная книга</h1>
    </header>
    <nav class="nav">
        <a href="/">Главная</a>
        <a href="/soups">Супы</a>
        <a href="/main">Основные блюда</a>
        <a href="/snacks">Закуски</a>
        <a href="/exotic">Экзотика</a>
    </nav>
    <main class="container">
        {{content | safe}}
    </main>
    <footer class="footer">
        <p>Присылайте свои рецепты на почту: recepts35@vksit.ru</p>
    </footer>
</body>
</html>
'''

home_content = '''
<h2>Добро пожаловать на кулинарный сайт!</h2>
<p>Здесь вы найдете лучшие рецепты для домашней кухни.</p>
<p>Выберите категорию в меню выше или воспользуйтесь поиском:</p>
<form class="search-form" action="/search" method="get">
    <input class="search-input" type="text" name="query" placeholder="Введите название рецепта..." required>
    <button class="search-button" type="submit">Поиск</button>
</form>
<ul>
    <li><strong>Супы</strong> - горячие первые блюда</li>
    <li><strong>Основные блюда</strong> - вторые блюда</li>
    <li><strong>Закуски</strong> - легкие блюда и снеки</li>
    <li><strong>Экзотика</strong> - необычные рецепты</li>
</ul>
'''

recipes_content = '''
<h2>{{category_title}}</h2>
{% for recipe in recipes %}
<div class="recipe-card">
    <h3 class="recipe-title">{{recipe.title}}</h3>
    <div class="recipe-section">
        <h4>Ингредиенты:</h4>
        <p>{{recipe.ingredients}}</p>
    </div>
    <div class="recipe-section">
        <h4>Способ приготовления:</h4>
        <p>{{recipe.instructions.replace('\n', '<br>') | safe}}</p>
    </div>
</div>
{% endfor %}
'''

recipe_not_found_content = '''
<div class="not-found">
    <h2>Рецепт не найден</h2>
    <p>Попробуйте другой запрос или выберите категорию из меню.</p>
</div>
'''


@app.route('/')
def home():
    return render_template_string(base_template,
                                  title="Главная",
                                  content=home_content)


@app.route('/search')
def search():
    query = request.args.get('query', '')
    recipe = Recipe.query.filter_by(title=query).first()
    if recipe:
        return redirect(url_for('recipe_detail', recipe_id=recipe.id))
    else:
        return render_template_string(base_template,
                                      title="Поиск",
                                      content=recipe_not_found_content)


@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template_string(base_template,
                                  title=recipe.title,
                                  content=render_template_string(recipes_content,
                                                                 category_title=recipe.title,
                                                                 recipes=[recipe]))


@app.route('/soups')
def soups():
    recipes = Recipe.query.filter_by(category='soup').all()
    return render_template_string(base_template,
                                  title="Рецепты супов",
                                  content=render_template_string(recipes_content,
                                                                 category_title="Рецепты супов",
                                                                 recipes=recipes))


@app.route('/main')
def main_dishes():
    recipes = Recipe.query.filter_by(category='main').all()
    return render_template_string(base_template,
                                  title="Основные блюда",
                                  content=render_template_string(recipes_content,
                                                                 category_title="Основные блюда",
                                                                 recipes=recipes))


@app.route('/snacks')
def snacks():
    recipes = Recipe.query.filter_by(category='snack').all()
    return render_template_string(base_template,
                                  title="Закуски",
                                  content=render_template_string(recipes_content,
                                                                 category_title="Рецепты закусок",
                                                                 recipes=recipes))


@app.route('/exotic')
def exotic():
    recipes = Recipe.query.filter_by(category='exotic').all()
    return render_template_string(base_template,
                                  title="Экзотические рецепты",
                                  content=render_template_string(recipes_content,
                                                                 category_title="Экзотические рецепты",
                                                                 recipes=recipes))


if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)

