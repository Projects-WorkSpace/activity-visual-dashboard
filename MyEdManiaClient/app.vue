<script setup lang="ts">
useHead({
    title: 'My EdMania Client app',
    meta: [{ name: 'description', content: 'Full app ecommerce' }],
    link: [
        { href: 'https://fonts.googleapis.com', rel: 'preconnect' },
        { href: 'https://fonts.gstatic.com', rel: 'preconnect' },
        {
            href: 'https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700;800;900&family=Nunito:wght@200;400;500;600;700;800;900&family=PT+Sans:wght@400;700&display=swap',
            rel: 'stylesheet',
        },
    ],
});
if (process.client) {
    await new Promise((resolve) => setTimeout(resolve, 2000));
}
</script>
<template>
    <main class="w-screen h-screen flex flex-col">
        <NuxtLayout>
            <NuxtPage />
        </NuxtLayout>
    </main>
</template>

<style>
.page-enter-active,
.page-leave-active {
    transition: all 0.4s;
}
.page-enter-from,
.page-leave-to {
    opacity: 0;
    filter: blur(1rem);
}

.layout-enter-active,
.layout-leave-active {
    transition: all 0.4s;
}
.layout-enter-from,
.layout-leave-to {
    /* filter: grayscale(1); */
    opacity: 0;
}
</style>
