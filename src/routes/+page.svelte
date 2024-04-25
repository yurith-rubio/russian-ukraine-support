<script>
    import Map from '../components/Map.svelte';
    import Spendings from "../components/Spendings.svelte";

</script>

<section class="section">
    <h2 class="padding-sides">Military spendings</h2>
    <p class="padding-sides">$B / %GDP</p>

    <Spendings />
</section>

<section class="section">
<h2 class="padding-sides">Russia support around the globe</h2>

<Map />

<p class="article__body-text padding-sides">
<a href="https://www.economist.com/graphic-detail/2023/03/31/who-are-russias-supporters" alt="who-are-russias-supporters">Source of information</a>
</p>

<p class="article__body-text padding-sides">Original article from <a href="https://informationisbeautiful.net/visualizations/ukraine-russian-war-infographics-data-visuals/#two-years" alt="ukraine-russian-war-infographics-data-visuals">source</a>. Design and development by Yurith Rubio</p>
</section>
<style>
    .section {
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    h2 {
        color: #07203f;
        text-align: center;
        font-size: 2rem;
    }
    @media screen and (min-width: 768px) {
        h2 {
            font-size: 4rem;
        }
    }
</style>