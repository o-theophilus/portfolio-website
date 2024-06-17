<script>
	import { onMount } from 'svelte';
	import { module, user, portal } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Rating from './rating_rating.svelte';

	export let post_key;
	let ratings = [];
	let o_rating = 0;
	let my_rating = 0;
	let loading = true;

	const calc_rating = () => {
		o_rating = 0;
		for (const i in ratings) {
			o_rating += ratings[i].rating;
			if (ratings[i].user_key == $user.key) {
				my_rating = ratings[i].rating;
			}
		}
	};

	$: if ($portal) {
		if ($portal.for == 'rating') {
			ratings = $portal.data;
			calc_rating();
		}

		if (['rating'].includes($portal.for)) {
			$portal = {};
		}
	}

	onMount(async () => {
		loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/rating/${post_key}`);
		resp = await resp.json();
		if (resp.status == 200) {
			ratings = resp.ratings;
		}
		loading = false;
		calc_rating();
	});
</script>

{#if $user.login}
	<Button
		size="small"
		on:click={() => {
			$module = {
				module: Rating,
				post_key,
				ratings
			};
		}}
	>
		<Icon icon="hotel_class" />
		Rate: {my_rating} | Overall Rating: {o_rating}
	</Button>
{/if}

<style>
</style>
