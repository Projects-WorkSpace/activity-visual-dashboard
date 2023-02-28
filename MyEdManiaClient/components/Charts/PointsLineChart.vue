<script setup lang="ts">
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { UniversalTransition } from 'echarts/features';
import { LineChart } from 'echarts/charts';
import { TitleComponent, ToolboxComponent, TooltipComponent, GridComponent, LegendComponent } from 'echarts/components';
import VChart from 'vue-echarts';
import { PointSeries } from '~~/Types/General';

use([TitleComponent, ToolboxComponent, TooltipComponent, GridComponent, LegendComponent, LineChart, CanvasRenderer, UniversalTransition]);

const props = defineProps<{
    Activities: string[];
    Weekdays: string[];
    point_series: PointSeries[];
}>();

// provide(THEME_KEY, 'dark');
const option = ref({
    tooltip: {
        trigger: 'axis',
    },
    legend: {
        data: props.Activities,
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
        data: props.Weekdays,
    },
    yAxis: {
        type: 'value',
        boundaryGap: false,
        name: 'Points',
    },
    series: props.point_series,
});
</script>
<template>
    <div id="chart-container" class="w-full h-[350px] sm:h-[500px] border-neutral-200 rounded-lg bg-gray-50 px-2 py-4">
        <v-chart :style="{ width: '100%', height: '100%' }" :option="option" autoresize />
    </div>
</template>
