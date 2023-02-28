<script setup lang="ts">
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { UniversalTransition } from 'echarts/features';
import { LineChart } from 'echarts/charts';
import { TitleComponent, ToolboxComponent, TooltipComponent, GridComponent, LegendComponent } from 'echarts/components';
import VChart from 'vue-echarts';

use([TitleComponent, ToolboxComponent, TooltipComponent, GridComponent, LegendComponent, LineChart, CanvasRenderer, UniversalTransition]);

const option = ref({
    tooltip: {
        trigger: 'axis',
    },
    legend: {
        data: [''],
        height: 'auto',
    },
    grid: {
        left: '2%',
        right: '2%',
        bottom: '1%',
        containLabel: true,
    },
    toolbox: {
        feature: {
            saveAsImage: {},
        },
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    },
    yAxis: {
        type: 'value',
        boundaryGap: false,
    },
    series: [
        {
            name: '',
            type: 'line',
            data: [0, 0, 0, 0, 0, 0, 0],
            smooth: true,
        },
    ],
});
</script>
<template>
    <div class="w-full">
        <div id="chart-container" class="w-full h-[350px] sm:h-[500px] border-neutral-200 rounded-lg bg-gray-50 px-2 py-4">
            <v-chart :style="{ width: '100%', height: '100%' }" :option="option" autoresize />
        </div>
    </div>
</template>
