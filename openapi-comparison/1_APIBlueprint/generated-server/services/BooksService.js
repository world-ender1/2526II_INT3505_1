/* eslint-disable no-unused-vars */
const Service = require('./Service');

/**
* Add a New Book
*
* body AddANewBookRequest  (optional)
* returns Add_a_New_Book_201_response
* */
const add a New Book = ({ body }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        body,
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);
/**
* Get a Book by ID
*
* id BigDecimal Book ID
* returns Get_a_Book_by_ID_200_response
* */
const get a Book by ID = ({ id }) => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
        id,
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);
/**
* List All Books
*
* returns List
* */
const list All Books = () => new Promise(
  async (resolve, reject) => {
    try {
      resolve(Service.successResponse({
      }));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 405,
      ));
    }
  },
);

module.exports = {
  add a New Book,
  get a Book by ID,
  list All Books,
};
