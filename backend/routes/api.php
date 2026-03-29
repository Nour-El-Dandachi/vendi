<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\Customer\ProductController;
use App\Http\Controllers\Customer\CartController;
use App\Http\Controllers\Customer\OrderController;
use App\Http\Controllers\Customer\AddressController;
use App\Http\Controllers\Customer\NotificationController;
use App\Http\Controllers\Vendor\ProductController as VendorProductController;
use App\Http\Controllers\Vendor\OrderController as VendorOrderController;
use App\Http\Controllers\Admin\UserController;
use App\Http\Controllers\Admin\ProductController as AdminProductController;
use App\Http\Controllers\Admin\OrderController as AdminOrderController;
use App\Http\Controllers\Vendor\StoreController;

Route::group(["prefix" => "v0.1"], function () {

    Route::group(["middleware" => "auth:sanctum"], function () {

        Route::group(["prefix" => "customer"], function () {
            Route::get('/products/{id?}', [ProductController::class, "getAllProducts"]);
            Route::get('/cart/{id?}', [CartController::class, "getCartItems"]);
            Route::post('/add_update_cart/{id?}', [CartController::class, "addOrUpdateCartItem"]);
            Route::get('/orders/{id?}', [OrderController::class, "getAllOrders"]);
            Route::post('/place_order', [OrderController::class, "placeOrder"]);
            Route::get('/addresses/{id?}', [AddressController::class, "getAllAddresses"]);
            Route::post('/add_update_address/{id?}', [AddressController::class, "addOrUpdateAddress"]);
            Route::get('/notifications/{id?}', [NotificationController::class, "getAllNotifications"]);
        });

        Route::group(["prefix" => "vendor"], function () {
            Route::get('/products/{id?}', [VendorProductController::class, "getAllProducts"]);
            Route::post('/add_update_product/{id?}', [VendorProductController::class, "addOrUpdateProduct"]);
            Route::get('/orders/{id?}', [VendorOrderController::class, "getAllOrders"]);
            Route::get('/stores/{id?}', [StoreController::class, "getAllStores"]);
            Route::post('/add_update_store/{id?}', [StoreController::class, "addOrUpdateStore"]);
            Route::delete('/delete_store/{id}', [StoreController::class, "deleteStore"]);
            Route::delete('/delete_product/{id}', [VendorProductController::class, "deleteProduct"]);
        });

        Route::group(["prefix" => "admin"], function () {
            Route::get('/users/{id?}', [UserController::class, "getAllUsers"]);
            Route::get('/products/{id?}', [AdminProductController::class, "getAllProducts"]);
            Route::get('/orders/{id?}', [AdminOrderController::class, "getAllOrders"]);
        });

        Route::post('/logout', [AuthController::class, 'logout']);
    });

    Route::group(["prefix" => "guest"], function () {
        Route::post("/login", [AuthController::class, "login"]);
        Route::post("/register", [AuthController::class, "register"]);
    });
});