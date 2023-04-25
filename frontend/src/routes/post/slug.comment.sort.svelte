<script>
	import { api_url, portal, loading, _user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';

	export let post_key;
	let error = '';

	let form = { ...$_user.setting };
	let sort = {
		date: ['old', 'new'],
		vote: ['low', 'high']
	};

	let changed = false;
	const compare = () => {
		changed = false;
		if (
			form.sort_comment_by != $_user.setting.sort_comment_by ||
			form.sort_comment_reverse != $_user.setting.sort_comment_reverse
		) {
			changed = true;
		}
	};

	const submit = async () => {
		error = '';

		$loading = `Sorting comment . . .`;
		const resp = await fetch(`${api_url}/setting`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				changed = false;
				$_user = data.data.user;
				submit_sort();
			} else {
				$loading = false;
				error = data.message;
			}
		}
	};

	const submit_sort = async () => {
		const resp = await fetch(`${api_url}/comment/${post_key}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			}
		});
		$loading = false;

		if (resp.ok) {
			const data = await resp.json();

			if (data.status == 200) {
				portal({
					for: 'comment',
					data: data.data.comments
				});
			} else {
				error = data.message;
			}
		}
	};
</script>

<section>
	<div class="block">
		<div class="sort">
			sort by:

			<select
				bind:value={form.sort_comment_by}
				on:change={() => {
					compare();
				}}
			>
				{#each Object.entries(sort) as [name, op]}
					<option value={name}>{name}</option>
				{/each}
			</select>
			<select
				bind:value={form.sort_comment_reverse}
				on:change={() => {
					compare();
				}}
			>
				<option value={true}>{sort[form.sort_comment_by][1]}-{sort[form.sort_comment_by][0]}</option>
				<option value={false}>{sort[form.sort_comment_by][0]}-{sort[form.sort_comment_by][1]}</option>
			</select>
		</div>

		{#if changed}
			<Button
				class="tiny"
				on:click={() => {
					submit();
				}}
			>
				Ok
			</Button>
		{/if}
	</div>

	{#if error}
		<span class="error">
			{error}
		</span>
	{/if}
</section>

<style>
	.block,
	.sort {
		display: flex;
		align-items: center;
	}
	.block {
		gap: var(--gap2);
	}

	select {
		background-color: transparent;
		border: none;
		color: var(--accent2);
		cursor: pointer;
	}
	
</style>
