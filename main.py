from website import create_app

__author__ = 'Ivan Boldyrev'

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
