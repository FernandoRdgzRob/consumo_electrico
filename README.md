# Electrical Consumption Application

## Project Description
Research project led by Ph.D. Blanca Nydia Pérez, designed to monitor the electrical consumption of household appliances.


## Technologies used

### Backend

Flask: Python module that lets you develop web applications easily.

Ariadne: Ariadne is a Python library for implementing GraphQL servers.

PostgreSQL: PostgreSQL is a free and open-source relational database management system (RDBMS) emphasizing extensibility and SQL compliance.

### Frontend

React: A JavaScript library for building user interfaces You can learn more in the React Documentation.

Material UI: Customizable, and accessible library of foundational and advanced components, enabling you to develop React applications faster.

React Router: React Router is a fully-featured client and server-side routing library for React, a JavaScript library for building user interfaces. React Router runs anywhere React runs; on the web, on the server with node.js, and on React Native.

React Hook Form: Performant, flexible and extensible forms with easy-to-use validation.

Notistack: Notistack is a Snackbar library which makes it extremely easy to display notifications on your web apps. It is highly customizable and enables you to stack snackbars/toasts on top of one another.

### API

GraphQL: GraphQL is an open-source data query and manipulation language for APIs, and a runtime for fulfilling queries with existing data.


## Project Setup

```git clone https://github.com/luisedgarflores/electrical_consumption.git```

### Database

```sudo -u postgres psql postgres```

```CREATE DATABASE electrical_consumption;```

```CREATE USER ec_user WITH ENCRYPTED PASSWORD ‘12341234’;```

```GRANT ALL PRIVILEGES ON DATABASE electrical_consumption to ec_user;```


### Backend

In electrical_consumption/backend folder:

```python3 -m pip install -r requirements.txt```

```flask run```


### Frontend

In electrical_consumption/frontend folder:

```npm install```

```npm start```