<?php

namespace App\Services;

use App\Models\Product;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class ProductService
{
    static function getAllProducts($id = null)
    {
        if (!$id) {
            return Product::with(['vendor', 'store'])->get();
        }

        return Product::with(['vendor', 'store'])->find($id);
    }

    static function createOrUpdateProduct($data, $product)
    {
        if (isset($data['base64']) && isset($data['file_name'])) {
            $base64String = $data['base64'];

            if (Str::contains($base64String, ';base64,')) {
                [$meta, $base64String] = explode(';base64,', $base64String);
            }

            $decoded = base64_decode($base64String);

            $filename = uniqid() . '_' . preg_replace('/\s+/', '_', $data['file_name']);
            $folder = 'product_images';
            $fullPath = $folder . '/' . $filename;

            Storage::disk('public')->put($fullPath, $decoded);

            $product->image = $fullPath;
        }

        $product->vendor_id = $data['vendor_id'] ?? $product->vendor_id;
        $product->store_id = $data['store_id'] ?? $product->store_id;
        $product->name = $data['name'] ?? $product->name;
        $product->description = $data['description'] ?? $product->description;
        $product->category = $data['category'] ?? $product->category;
        $product->sku = $data['sku'] ?? $product->sku;
        $product->price = $data['price'] ?? $product->price;
        $product->stock_quantity = $data['stock_quantity'] ?? $product->stock_quantity;
        $product->status = $data['status'] ?? $product->status;

        $product->save();
        return $product;
    }

    static function deleteProduct($product)
    {
        return $product->delete();
    }
}