<?php

namespace App\Http\Controllers\Admin;

use Exception;
use App\Services\AdminService;
use App\Http\Controllers\Controller;

class ProductController extends Controller
{
    public function getAllProducts($id = null)
    {
        try {
            $products = AdminService::getAllProducts($id);
            return $this->responseJSON($products);
        } catch (Exception $e) {
            return $this->responseJSON(null, "Failed to retrieve products.", 500);
        }
    }

    public function deleteProduct($id)
    {
        try {
            $product = AdminService::getAllProducts($id);

            if (!$product) {
                return $this->responseJSON(null, "Product not found.", 404);
            }

            $deleted = AdminService::deleteProduct($product);

            if ($deleted) {
                return $this->responseJSON(null);
            }

            return $this->responseJSON(null, "Failed to delete product.", 400);
        } catch (Exception $e) {
            return $this->responseJSON(null, "Server error while deleting product.", 500);
        }
    }
}