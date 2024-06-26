<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { module, user } from '$lib/store.js';

	import Content from '$lib/content.svelte';
	import Marked from '$lib/marked.svelte';
	import Meta from '$lib/meta.svelte';
	import Button from '$lib/button/button.svelte';
	import BRound from '$lib/button/round.svelte';
	import Tags from './tags.svelte';
	import Toggle from '$lib/toggle.svelte';
	import Icon from '$lib/icon.svelte';
	import Log from '$lib/log.svelte';
	import Datetime from '$lib/datetime.svelte';

	import Title from './_title.svelte';
	import Description from './_description.svelte';
	import Edit_Tags from './_tags.svelte';
	import Edit_Content from './_content.svelte';
	import Edit_Date from './_date.svelte';
	import Edit_Status from './_status.svelte';
	import Manage_Photo from './_photo.svelte';
	import Rating from './_rating.svelte';

	import Share from './_share.svelte';
	import Refresh from './refresh.svelte';
	import Like from './like.svelte';

	import Comment from './comment/index.svelte';
	import Similar from './similar.svelte';
	import Highlight from './highlight.svelte';
	import Author from './author.svelte';

	export let data;
	$: post = data.post;
	let tags = [];
	let edit_mode = false;
	let admin = false;

	let content = '';
	let photo_count = 1;

	const process = (_in) => {
		if (!_in) {
			_in = '';
		}

		content = _in;
		photo_count = 1;
		let exist = content.search(/{#photo}/) >= 0;
		while (exist) {
			let i = `![${post.title}](${post.photos[photo_count]})`;
			content = content.replace(/{#photo}/, i);
			exist = content.search(/{#photo}/) >= 0;
			photo_count = photo_count + 1;
		}
	};

	const update = async (data) => {
		post = data;
	};

	let my_rating = null;
	const update_my_rating = async (data) => {
		my_rating = data;
	};

	onMount(async () => {
		if ($page.url.searchParams.has('edit') && admin) {
			$page.url.searchParams.delete('edit');
			edit_mode = true;

			window.history.replaceState(history.state, '', $page.url.href);
		}
		process(post.content);

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/admin/permission/post:edit`);
		resp = await resp.json();
		if (resp.status == 200) {
			admin = $user.permissions.some((x) => resp.permissions.includes(x));
		}
	});

	let author;
	let comment;
	let similar;
	const refresh = async () => {
		process(post.content);
		my_rating = null;
		author.reset();
		comment.reset();
		similar.reset();
		await author.refresh();
		await comment.refresh();
		await similar.refresh();
	};
</script>

{#key post.key}
	<Log action={'viewed'} entity_key={post.key} entity_type={'post'} />
	<Meta title={post.title} description={post.description} image={post.photos[0]} />
	<Refresh on:refresh={refresh} />
{/key}

<Content>
	{#if admin}
		<div class="toggle">
			<Toggle
				state_1="off"
				state_2="edit"
				active={edit_mode}
				on:click={() => {
					edit_mode = !edit_mode;
				}}
			/>
		</div>
	{/if}
	<div class="img">
		<img src={post.photos[0] || ''} alt={post.title} onerror="this.src='/site/no_photo.png'" />
		<div class="line">
			{#if $user.permissions.includes('post:edit_photos') && edit_mode}
				<BRound
					icon="photo"
					on:click={() => {
						$module = {
							module: Manage_Photo,
							post,
							photo_count,
							update
						};
					}}
				/>
			{/if}
		</div>
	</div>

	<div class="ititle">
		{#if $user.permissions.includes('post:edit_title') && edit_mode}
			<BRound
				icon="edit"
				on:click={() => {
					$module = {
						module: Title,
						post,
						update
					};
				}}
			/>
		{/if}
		<strong>
			{post.title}
		</strong>
	</div>

	{#if $user.permissions.includes('post:edit_date') && edit_mode}
		<hr />
		<BRound
			icon="edit"
			on:click={() => {
				$module = {
					module: Edit_Date,
					post,
					update
				};
			}}
		/>
	{/if}
	<span class="date">
		<Datetime datetime={post.date} />
	</span>

	{#if $user.permissions.includes('post:edit_description') && edit_mode}
		<hr />
		<BRound
			icon="edit"
			icon_size={15}
			on:click={() => {
				$module = {
					module: Description,
					post,
					update
				};
			}}
		/>
		<div class="margin">
			{#if post.description}
				{post.description}
			{:else}
				No description
			{/if}
		</div>
	{/if}

	<hr />

	{#if $user.permissions.includes('post:edit_content') && edit_mode}
		<BRound
			icon="edit"
			icon_size={15}
			on:click={() => {
				$module = {
					module: Edit_Content,
					post,
					update
				};
			}}
		/>
	{/if}
	{#if post.content}
		<Marked {content} />
		<br />
	{:else if edit_mode}
		<div class="margin">No content</div>
	{/if}

	<div class="line">
		<Like
			name="post"
			entity={post}
			on:update={(e) => {
				post = e.detail.post;
			}}
		/>

		{#if $user.login}
			<Button
				size="small"
				on:click={() => {
					$module = {
						module: Rating,
						post_key: post.key,
						my_rating,
						update_my_rating,
						update
					};
				}}
			>
				<Icon icon="hotel_class" />
				Rate: {parseFloat(post.rating)}/{post.ratings}
			</Button>
		{/if}

		<Button
			size="small"
			on:click={() => {
				$module = {
					module: Share,
					post
				};
			}}
		>
			<Icon icon="share" />
			Share
		</Button>
	</div>

	<Author {post} bind:this={author} {edit_mode} />

	{#if post.tags.length > 0 || ($user.permissions.includes('post:edit_tags') && edit_mode)}
		<hr />
	{/if}

	{#if $user.permissions.includes('post:edit_tags') && edit_mode}
		<BRound
			icon="edit"
			icon_size={15}
			on:click={() => {
				$module = {
					module: Edit_Tags,
					post,
					tags_in: tags,
					update
				};
			}}
		/>
	{/if}

	{#if post.tags.length > 0}
		<Tags tags={post.tags} />
	{:else if edit_mode}
		<div class="margin">No tag</div>
	{/if}

	{#if edit_mode && ($user.permissions.includes('post:edit_status') || ($user.permissions.includes('post:edit_highlight') && post.status == 'active'))}
		<hr />
		<div class="line">
			{#if $user.permissions.includes('post:edit_status') && edit_mode}
				<Button
					size="small"
					on:click={() => {
						$module = {
							module: Edit_Status,
							post,
							update
						};
					}}
				>
					<Icon icon="edit" size="16" />
					|
					<span>
						Status: <strong>{post.status}</strong>
					</span>
				</Button>
			{/if}
			{#if $user.permissions.includes('post:edit_highlight') && edit_mode && post.status == 'active'}
				<Highlight post_key={post.key} />
			{/if}
		</div>
	{/if}

	<hr />

	<Comment {post} bind:this={comment} />
	<Similar post_key={post.key} bind:this={similar} />
</Content>

<style>
	.img {
		position: relative;
	}

	img {
		display: block;

		width: 100%;
		margin: var(--sp2) 0;
		border-radius: var(--sp1);

		background-color: var(--bg2);
	}
	.img .line {
		position: absolute;
		bottom: var(--sp1);
		left: var(--sp1);
	}

	.ititle {
		margin-top: var(--sp3);
	}
	.date {
		font-size: small;
		margin-bottom: var(--sp3);
	}

	.margin {
		margin: var(--sp2) 0;
	}

	hr {
		margin: var(--sp2) 0;
	}

	.line {
		display: flex;
		align-items: center;
		gap: var(--sp1);
	}
</style>
