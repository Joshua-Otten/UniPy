# Example React-Express App

## Submission Information

## Project Overview

This repo contains a barebones Node.js app using [Express 4](http://expressjs.com/) and a barebones React app with a single component. You will use this as the "base" version of your Microserivce + Front-end application for HW Assignment #3. You will simply create a copy of this repo through GitHub classroom and then work in that repo. 

## Running this Project Locally

Make sure you have [Node.js](http://nodejs.org/) and (optionally) the [Heroku CLI](https://cli.heroku.com/) installed. You only need the Heroku CLI installed if you plan to deploy the project from the CLI instead of the Heroku web interface. See the [HW Assignment #3 instructions](https://cs.gmu.edu/~kpmoran/teaching/swe-432-s23/hw3) for more details.

*Note the following commands assume a Unix-based enviornment. If you are on windows, you may need to use something such as Windows Subsystem for Linux (https://docs.microsoft.com/en-us/windows/wsl/about).*

```sh
$ git clone <repo-name>
$ cd <repo-name>
$ npm install
$ npm run setup
$ npm start
```

After executing these commands, your express backend and React frontend should now be running on [localhost:3000](http://localhost:3000/). You can visit this page in your web browser to view your front-end user interface. You can also access your microservice endpoints (e.g., [localhost:6000/cities](http://localhost:6000/cities). Please see the [HW #3 instructions](https://cs.gmu.edu/~kpmoran/teaching/swe-432-s23/hw3) for more information on how this works.

## Testing with Continuous Integration

**Note that you are not required to test your project with Jest for HW3, however, we have enabled this functionality in case you would like to use it. If you would like to remove the tests, you can remove the `.github` directory from the repo.**

Currently, this repo is set up to run the Jest tests in the `app.test.js` file upon each commit to the `main` branch of the repository. If any of the tests fail, the CI process will fail and this will be indicated with red "X" on the main page of your repo, and GitHub will likely also send you a notification email that your automated tests have failed.

Currently, the tests are configured to run by getting deployed to a remote virtual server with an Ubuntu operating system, where the `npm install` and `npm test` commands are executed.

You can find the [GitHub Actions](https://github.com/features/actions) script for this CI job [here](.github/workflows/ci.yml) if you want to learn more.

## Additional Resources

For more information about using Node.js on Heroku, see these Heroku Dev Center articles:

- [React Tutorial](https://reactjs.org/tutorial/tutorial.html)
- [Express Documentation](https://expressjs.com/en/5x/api.html)
- [Supertest Documentation](https://www.npmjs.com/package/supertest)
- [Best Practices for Node.js Development](https://devcenter.heroku.com/articles/node-best-practices)
