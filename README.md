<h1>Cargo API service instruction<p>

<h2>Установка и запуск приложения</h2>
<section><ul>
<li>Клонируйте репозиторий<br><code>git clonehttps://github.com/CHRNVpy/cargo-api.git</code></li>
<li>Перейдите в директорию репозитория<br><code>cd Cargo</code></li>
<li>Создайте Docker контейнер<br><code>docker-compose up</code></li>
</ul>
</section>

<section>
<ul>После сборки контейнера Django сервер запустится автоматически.<br>
    Создайте миграции
    <li><code>docker exec &lt;название контейнера&gt; python manage.py makemigrations</code></li>
    <li><code>docker exec &lt;название контейнера&gt; python manage.py migrate</code></li>
    <li>Импортируйте данные о локациях<br>
        <code>docker exec &lt;название контейнера&gt; python manage.py import_locations uszips.csv</code></li>
    <li>Сгенерируйте транспорт<br>
        <code>docker exec &lt;название контейнера&gt; python manage.py generate cars &lt;количесто машин: int&gt;</code></li>
    <li>Сгенерируйте грузы (не обязательно)<br>
        <code>docker exec &lt;название контейнера&gt; python manage.py generate cargo &lt;количесто карго: int&gt;</code></li>
    <li>Запустите сервис для автоматического обновления локаций машин каждые 3 минуты (не обязательно)<br>
        <code>docker exec &lt;название контейнера&gt; cron</code></li>
</ul>
</section>

<h2>API ENDPOINTS</h2>
<p>BASE URL: <code>https://localhost:8000</code></p>
<section>
  <h3>Добавление груза</h3>
  <p><strong>ENDPOINT:</strong> <code>POST /api/cargo_add/</code></p>
  <p><strong>Parameters:</strong></p>
  <ul>
    <li><code>pick_up_location</code>: Location's zip code (integer)</li>
    <li><code>delivery_location</code>: Location's zip code (integer)</li>
    <li><code>weight</code>: Weight of the cargo (string)</li>
    <li><code>description</code>: Description of the cargo (string)</li>
  </ul>
  <p>Example Request Body:</p>
  <img src="images/cargo_add.png" alt="Cargo Add Example Request">
</section>
<section>
  <h3>Получение списка грузов</h3>
  <p><strong>ENDPOINT:</strong> <code>GET /api/cargo_list/</code></p>
  <p><strong>Parameters:</strong> (optional)</p>
  <ul>
    <li><code>weight</code>: Weight of the cargo (string)</li>
    <li><code>miles_to_cars</code>: Distance in miles to the cars (integer)</li>
  </ul>
  <p>Example Response:</p>
  <img src="images/cargo_list.png" alt="Cargo List Example Response">
</section>
<section>
  <h3>Получение информации о грузе по ID</h3>
  <p><strong>ENDPOINT:</strong> <code>GET /api/cargo/&lt;int:cargo_id&gt;/</code></p>
  <p>Example Response:</p>
  <img src="images/cargo_info.png" alt="Cargo Info Example Response 1">
  <img src="images/cargo_info2.png" alt="Cargo Info Example Response 2">
</section>
<section>
  <h3>Обновление локации авто</h3>
  <p><strong>ENDPOINT:</strong> <code>PUT /api/car_update/&lt;int:car_id&gt;/</code></p>
  <p><strong>Parameters:</strong></p>
  <ul>
    <li><code>current_location</code>: Location's zip code (integer)</li>
  </ul>
  <p>Example Request Body:</p>
  <img src="images/car_update.png" alt="Car Update Example Request">
</section>
<section>
  <h3>Обновление информации о грузе (вес, описание)</h3>
  <p><strong>ENDPOINT:</strong> <code>PUT /api/cargo_update/&lt;int:cargo_id&gt;/</code></p>
  <p><strong>Parameters:</strong></p>
  <ul>
    <li><code>weight</code>: Weight of the cargo (integer)</li>
    <li><code>description</code>: Description of the cargo (string)</li>
  </ul>
  <p>Example Request Body:</p>
  <img src="images/cargo_update.png" alt="Cargo Update Example Request">
</section>
<section>
  <h3>Удаление груза</h3>
<p><strong>ENDPOINT:</strong> <code>GET /api/cargo_delete/&lt;int:cargo_id&gt;/</code></p>
  <p>Example Response:</p>
  <img src="images/cargo_delete.png" alt="Cargo Delete Example Response">
</section>