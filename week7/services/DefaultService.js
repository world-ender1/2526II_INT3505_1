/* eslint-disable no-unused-vars */
const Service = require('./Service');
const Product = require('../models/Product');
const crypto = require('crypto');

/**
* Create a product
*
* productInput ProductInput 
* returns Product
* */
const createProduct = ({ productInput }) => new Promise(
  async (resolve, reject) => {
    try {
      const newProduct = new Product({
        ...productInput,
        id: crypto.randomUUID()
      });
      const savedProduct = await newProduct.save();
      resolve(Service.successResponse(savedProduct));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 500,
      ));
    }
  },
);

/**
* Delete a product
*
* id String 
* no response value expected for this operation
* */
const deleteProduct = ({ id }) => new Promise(
  async (resolve, reject) => {
    try {
      const deletedProduct = await Product.findOneAndDelete({ id });
      if (!deletedProduct) {
        return reject(Service.rejectResponse('Product not found', 404));
      }
      resolve(Service.successResponse('Deleted successfully', 204));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 500,
      ));
    }
  },
);

/**
* Get a product by ID
*
* id String 
* returns Product
* */
const getProductById = ({ id }) => new Promise(
  async (resolve, reject) => {
    try {
      const product = await Product.findOne({ id });
      if (!product) {
        return reject(Service.rejectResponse('Product not found', 404));
      }
      resolve(Service.successResponse(product));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 500,
      ));
    }
  },
);

/**
* Get all products
*
* returns List
* */
const getProducts = () => new Promise(
  async (resolve, reject) => {
    try {
      const products = await Product.find({});
      resolve(Service.successResponse(products));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 500,
      ));
    }
  },
);

/**
* Update a product
*
* id String 
* productInput ProductInput 
* returns Product
* */
const updateProduct = ({ id, productInput }) => new Promise(
  async (resolve, reject) => {
    try {
      const updatedProduct = await Product.findOneAndUpdate(
        { id },
        { ...productInput },
        { new: true, runValidators: true }
      );
      if (!updatedProduct) {
        return reject(Service.rejectResponse('Product not found', 404));
      }
      resolve(Service.successResponse(updatedProduct));
    } catch (e) {
      reject(Service.rejectResponse(
        e.message || 'Invalid input',
        e.status || 500,
      ));
    }
  },
);

module.exports = {
  createProduct,
  deleteProduct,
  getProductById,
  getProducts,
  updateProduct,
};
