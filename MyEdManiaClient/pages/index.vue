<template>
    <section class="w-full flex flex-col h-screen bg-cover">
        <div id="hero" class="w-full grid grid-cols-1 px-2 sm:px-8 lg:px-20 xl:px-40 gap-y-12">
            <div class="col-span-1 h-full flex flex-col gap-y-6 items-center justify-start pt-12 sm:pt-20 px-4 sm:px-0 text-gray-50">
                <h3
                    class="text-5xl lg:text-7xl font-extrabold text-transparent bg-clip-text text-center bg-gradient-to-r to-emerald-300 from-gray-100"
                >
                    Your child is a Hero!
                </h3>
                <p class="text-base text-center sm:text-lg">Join us now and access guided daily reports for amazing kids activities.</p>
                <div id="auth-redirects" class="flex flex-row gap-x-6 items-center">
                    <button
                        @click="() => useRouter().push('/users/register')"
                        type="button"
                        class="text-neutral-800 bg-gray-100 hover:bg-gray-200 focus:ring-2 focus:ring-blue-300 font-medium rounded-lg text-base sm:text-lg px-10 py-2.5 transition duration-200"
                    >
                        Start now
                    </button>
                </div>
            </div>
            <div class="col-span-1 flex flex-col items-center justify-center gap-y-2 relative">
                <div class="flex flex-col items-center w-full">
                    <svg aria-hidden="true" viewBox="0 0 418 42" class="h-10 w-full sm:w-1/2 fill-blue-300/70" preserveAspectRatio="none">
                        <path
                            d="M203.371.916c-26.013-2.078-76.686 1.963-124.73 9.946L67.3 12.749C35.421 18.062 18.2 21.766 6.004 25.934 1.244 27.561.828 27.778.874 28.61c.07 1.214.828 1.121 9.595-1.176 9.072-2.377 17.15-3.92 39.246-7.496C123.565 7.986 157.869 4.492 195.942 5.046c7.461.108 19.25 1.696 19.17 2.582-.107 1.183-7.874 4.31-25.75 10.366-21.992 7.45-35.43 12.534-36.701 13.884-2.173 2.308-.202 4.407 4.442 4.734 2.654.187 3.263.157 15.593-.78 35.401-2.686 57.944-3.488 88.365-3.143 46.327.526 75.721 2.23 130.788 7.584 19.787 1.924 20.814 1.98 24.557 1.332l.066-.011c1.201-.203 1.53-1.825.399-2.335-2.911-1.31-4.893-1.604-22.048-3.261-57.509-5.556-87.871-7.36-132.059-7.842-23.239-.254-33.617-.116-50.627.674-11.629.54-42.371 2.494-46.696 2.967-2.359.259 8.133-3.625 26.504-9.81 23.239-7.825 27.934-10.149 28.304-14.005.417-4.348-3.529-6-16.878-7.066Z"
                        ></path>
                    </svg>
                </div>
                <div class="flex flex-col items-center justify-center w-full">
                    <img src="~/assets/Img/undraw_toy_car_-7-umw.svg" alt="" class="w-full sm:w-[40%] h-auto" />
                </div>
            </div>
        </div>
    </section>
</template>
