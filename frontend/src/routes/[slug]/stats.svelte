<script>
	import { module, user } from '$lib/store.js';

	import Button from '$lib/button/button.svelte';
	import Icon from '$lib/icon.svelte';
	import Rating from './rating_rating.svelte';
	import Loading from '$lib/loading.svelte';

	export let post_key;
	let ratings = [];
	let o_rating = 0;
	let rating = 0;
	let loading = true;

	const update = (_in) => {
		ratings = _in;
		o_rating = 0;
		rating = 0;
		for (const i in ratings) {
			o_rating += ratings[i].rating;
			if (ratings[i].user_key == $user.key) {
				rating = ratings[i].rating;
			}
		}
	};

	export const refresh = async () => {
		loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/rating/${post_key}`);
		resp = await resp.json();
		if (resp.status == 200) {
			update(resp.ratings);
		}
		loading = false;
	};
</script>

{#if $user.login}
	<Button
		size="small"
		on:click={() => {
			$module = {
				module: Rating,
				post_key,
				rating,
				update
			};
		}}
	>
		<Icon icon="hotel_class" />
		Rate: {rating} | Overall Rating: {o_rating}
	</Button>
{/if}

<style>
</style>
