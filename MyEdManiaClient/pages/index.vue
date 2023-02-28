<template>
    <section class="w-full flex flex-col">
        <div id="hero" class="w-full min-h-[94vh] bg-cover lg:grid grid-cols-2 px-2 sm:px-8 lg:px-20 xl:px-40">
            <div class="col-span-1 h-full flex flex-col gap-y-6 items-start justify-start pt-12 sm:pt-28 px-4 sm:px-0 text-gray-50">
                <h3
                    class="text-7xl sm:text-8xl md:text-9xl lg:text-8xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r to-emerald-300 from-gray-100"
                >
                    Your child is a Hero!
                </h3>
                <p class="text-lg sm:text-xl">
                    Join us now and access guided daily <br />
                    reports for amazing kids activities.
                </p>
                <div id="auth-redirects" class="w-full flex flex-row gap-x-6 items-center">
                    <!-- <button
                        @click="useRouter().push('/users/register')"
                        type="button"
                        class="text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-200 font-medium rounded-full text-base px-5 py-2"
                    >
                        Start now
                    </button> -->
                    <button
                        type="button"
                        class="text-white bg-gradient-to-br from-purple-600 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"
                    >
                        Purple to Blue
                    </button>
                </div>
            </div>
            <div class="col-span-1 hidden lg:flex items-center justify-center relative">
                <svg
                    aria-hidden="true"
                    viewBox="0 0 418 42"
                    class="absolute top-[10%] left-0 h-[40px] w-full fill-blue-300/70"
                    preserveAspectRatio="none"
                >
                    <path
                        d="M203.371.916c-26.013-2.078-76.686 1.963-124.73 9.946L67.3 12.749C35.421 18.062 18.2 21.766 6.004 25.934 1.244 27.561.828 27.778.874 28.61c.07 1.214.828 1.121 9.595-1.176 9.072-2.377 17.15-3.92 39.246-7.496C123.565 7.986 157.869 4.492 195.942 5.046c7.461.108 19.25 1.696 19.17 2.582-.107 1.183-7.874 4.31-25.75 10.366-21.992 7.45-35.43 12.534-36.701 13.884-2.173 2.308-.202 4.407 4.442 4.734 2.654.187 3.263.157 15.593-.78 35.401-2.686 57.944-3.488 88.365-3.143 46.327.526 75.721 2.23 130.788 7.584 19.787 1.924 20.814 1.98 24.557 1.332l.066-.011c1.201-.203 1.53-1.825.399-2.335-2.911-1.31-4.893-1.604-22.048-3.261-57.509-5.556-87.871-7.36-132.059-7.842-23.239-.254-33.617-.116-50.627.674-11.629.54-42.371 2.494-46.696 2.967-2.359.259 8.133-3.625 26.504-9.81 23.239-7.825 27.934-10.149 28.304-14.005.417-4.348-3.529-6-16.878-7.066Z"
                    ></path>
                </svg>
                <img src="~/assets/Img/undraw_toy_car_-7-umw.svg" alt="" class="w-full h-auto" />
            </div>
        </div>
    </section>
</template>
